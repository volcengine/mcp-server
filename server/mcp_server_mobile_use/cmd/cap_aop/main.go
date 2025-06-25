package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"image"
	_ "image/png"
	"log"
	"os"
	"os/exec"
	"path"
	"strings"
	"time"

	uuid "github.com/satori/go.uuid"
	"github.com/volcengine/ve-tos-golang-sdk/v2/tos"
)

const (
	screenCapPath  = "/sdcard/tmp_screen_cap/"
	partSize       = int64(10 * 1024 * 1024) // 1M
	maxCurrencyNum = 5
)

type TosConfig struct {
	AccessKey    string
	SecretKey    string
	SessionToken string
	Bucket       string
	Region       string
	Endpoint     string
}

type ScreenShotRes struct {
	ScreenshotURL string `json:"screenshot_url"`
	Resolution    string `json:"resolution"`
}

var (
	tosConfig string
)

func main() {
	flag.StringVar(&tosConfig, "tos_conf", "", "tos conf")

	flag.Parse()

	if tosConfig == "" {
		flag.Usage()
		os.Exit(1)
	}
	decoded, err := base64.StdEncoding.DecodeString(tosConfig)
	if err != nil {
		log.Fatalf("Failed to decode tos config: %v", err)
		os.Exit(1)
	}
	var tosConfig TosConfig
	if err := json.Unmarshal(decoded, &tosConfig); err != nil {
		log.Fatalf("Failed to unmarshal tos config: %v", err)
		os.Exit(1)
	}
	if tosConfig.AccessKey == "" ||
		tosConfig.SecretKey == "" ||
		tosConfig.Bucket == "" ||
		tosConfig.Region == "" ||
		tosConfig.Endpoint == "" {
		log.Fatalf("Tos config is invalid")
		os.Exit(1)
	}

	ctx := context.Background()
	u := uuid.NewV4()
	uuidS := uuid.Must(u, nil).String()
	roundID := strings.ReplaceAll(uuidS, "-", "")
	objectKey := fmt.Sprintf("screenshot_%s_%s.png", roundID, time.Now().Format("20060102150405"))
	err = os.MkdirAll(screenCapPath, 0755)
	if err != nil {
		log.Fatalf("Failed to create directory: %v", err)
		os.Exit(1)
	}
	filePath := path.Join(screenCapPath, objectKey)

	cmd := exec.Command("/system/bin/screencap", "-b", "false", "-p", filePath)
	if err := cmd.Run(); err != nil {
		log.Fatalf("Failed to run screencap: %v", err)
		os.Exit(1)
	}
	defer func() {
		if err := os.Remove(filePath); err != nil {
			log.Printf("Warning: Failed to remove source file: %v", err)
		}
	}()

	// Get image resolution
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatalf("Failed to open image file: %v", err)
		os.Exit(1)
	}
	defer file.Close()

	img, _, err := image.DecodeConfig(file)
	if err != nil {
		log.Fatalf("Failed to decode image: %v", err)
		os.Exit(1)
	}
	resolution := fmt.Sprintf("%dx%d", img.Width, img.Height)

	cred := tos.NewStaticCredentials(tosConfig.AccessKey, tosConfig.SecretKey)

	if tosConfig.SessionToken != "" {
		cred.WithSecurityToken(tosConfig.SessionToken)
	}
	tosCli, err := tos.NewClientV2(tosConfig.Endpoint,
		tos.WithRegion(tosConfig.Region),
		tos.WithCredentials(cred),
		tos.WithEnableVerifySSL(false),
	)
	if err != nil || tosCli == nil {
		log.Fatalf("Failed to create tos client: %v", err)
		os.Exit(1)
	}

	_, err = tosCli.UploadFile(ctx, &tos.UploadFileInput{
		CreateMultipartUploadV2Input: tos.CreateMultipartUploadV2Input{
			Bucket: tosConfig.Bucket,
			Key:    objectKey,
		},
		FilePath:         filePath,
		PartSize:         partSize,
		TaskNum:          maxCurrencyNum,
		EnableCheckpoint: true,
	})
	if err != nil {
		log.Fatalf("Failed to upload file: %v", err)
		os.Exit(1)
	}

	output, err := tosCli.PreSignedURL(&tos.PreSignedURLInput{
		Bucket:     tosConfig.Bucket,
		Key:        objectKey,
		HTTPMethod: "GET",
		Expires:    60 * 60,
	})
	if err != nil {
		log.Fatalf("Failed to get pre-signed url: %v", err)
		os.Exit(1)
	}

	// Create response struct
	res := ScreenShotRes{
		ScreenshotURL: output.SignedUrl,
		Resolution:    resolution,
	}

	// Print the response as JSON
	jsonBytes, err := json.Marshal(res)
	if err != nil {
		log.Fatalf("Failed to marshal response: %v", err)
		os.Exit(1)
	}
	fmt.Println(string(jsonBytes))
}
