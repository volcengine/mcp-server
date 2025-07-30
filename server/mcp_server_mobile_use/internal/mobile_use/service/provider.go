package service

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"net/url"
	"strconv"
	"strings"

	"mcp_server_mobile_use/internal/mobile_use/consts"

	"github.com/volcengine/volc-sdk-golang/base"
	"github.com/volcengine/volc-sdk-golang/service/acep"
)

type MobileUseProvider interface {
	ScreenShot(ctx context.Context) (*ScreenShotResult, error)
	ScreenTap(ctx context.Context, x, y int) error
	ScreenSwipe(ctx context.Context, fromX, fromY, toX, toY int) error
	InputText(ctx context.Context, text string) error
	InputTextClear(ctx context.Context) error
	AutoInstallApp(ctx context.Context, downloadUrl string) error
	LaunchApp(ctx context.Context, packageName string) error
	CloseApp(ctx context.Context, packageName string) error
	KeyEvent(ctx context.Context, KeyEventType string) error

	ListApps(ctx context.Context) ([]AppItem, error)
}

type mobileUseImpl struct {
	acep   *acep.ACEP
	option *mobileUseOption
}

func NewMobileUseImpl(options ...Option) MobileUseProvider {
	mobileUseOption := defaultMobileUseOption()
	for _, option := range options {
		option(mobileUseOption)
	}

	if mobileUseOption.AccessKey == "" || mobileUseOption.SecretKey == "" {
		return nil
	}

	if mobileUseOption.ProductID == "" || mobileUseOption.DeviceID == "" {
		return nil
	}

	acepInst := acep.NewInstance()
	acepInst.SetHost(mobileUseOption.Host)
	acepInst.SetCredential(base.Credentials{
		AccessKeyID:     mobileUseOption.AccessKey,
		SecretAccessKey: mobileUseOption.SecretKey,
		SessionToken:    mobileUseOption.SessionToken,
	})

	impl := &mobileUseImpl{
		acep:   acepInst,
		option: mobileUseOption,
	}
	return impl
}

func (impl *mobileUseImpl) ScreenShot(ctx context.Context) (*ScreenShotResult, error) {
	tosConfig := TosConfig{
		AccessKey:    impl.option.TosAccessKey,
		SecretKey:    impl.option.TosSecretKey,
		SessionToken: impl.option.TosSessionToken,
		Bucket:       impl.option.Bucket,
		Region:       impl.option.Region,
		Endpoint:     impl.option.Endpoint,
	}
	tosBytes, _ := json.Marshal(tosConfig)
	tosConf := base64.StdEncoding.EncodeToString(tosBytes)
	command := fmt.Sprintf(consts.ACEPCommandScreenShotFormat, tosConf)
	output, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeRoot)
	if err != nil {
		return nil, err
	}
	if output == nil {
		return nil, fmt.Errorf("ScreenShot failed, output is nil")
	}
	screenshotResult, err := extractScreenshotURL(*output)
	if err != nil {
		return nil, fmt.Errorf("ScreenShot failed, invalid url err: %v", err)
	}
	if screenshotResult == nil {
		return nil, fmt.Errorf("ScreenShot failed, no screenshot url found")
	}
	return screenshotResult, nil
}

func (impl *mobileUseImpl) ScreenTap(ctx context.Context, x, y int) error {
	command := fmt.Sprintf(consts.ACEPCommandScreenTapFormat, x, y)
	_, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) ScreenSwipe(ctx context.Context, fromX, fromY, toX, toY int) error {
	command := fmt.Sprintf(consts.ACEPCommandScreenSwipeFormat, fromX, fromY, toX, toY, consts.ACEPScreenSwipeTimeMs)
	_, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) InputText(ctx context.Context, text string) error {
	command := consts.ACEPSelectInputMethod
	_, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	safeText := base64.StdEncoding.EncodeToString([]byte(text))

	inputText := fmt.Sprintf(consts.ACEPInputTextFormat, safeText)
	_, err = impl.runSyncCommand(ctx, inputText, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) InputTextClear(ctx context.Context) error {
	command := consts.ACEPKeyboardClear
	_, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) KeyEvent(ctx context.Context, KeyEventType string) error {
	keyEventCode, ok := consts.AndroidKeyEventMap[KeyEventType]
	if !ok {
		return fmt.Errorf("KeyEvent failed, invalid key event type: %s, don't support", KeyEventType)
	}
	command := fmt.Sprintf(consts.ACEPCommandKeyEventFormat, keyEventCode)
	_, err := impl.runSyncCommand(ctx, command, consts.ACEPCommandTypeShell)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) AutoInstallApp(ctx context.Context, downloadUrl string) error {
	request := &acep.AutoInstallAppBody{
		ProductID:   impl.option.ProductID,
		PodIDList:   []string{impl.option.DeviceID},
		DownloadURL: &downloadUrl,
	}
	response, err := impl.acep.AutoInstallApp(ctx, request)
	if err != nil {
		return err
	}
	if response == nil {
		return fmt.Errorf("AutoInstallApp failed, get nil response")
	}
	if len(response.Result.Jobs) == 0 {
		return fmt.Errorf("AutoInstallApp failed, get empty jobs")
	}
	return nil
}

func (impl *mobileUseImpl) LaunchApp(ctx context.Context, packageName string) error {
	request := &acep.LaunchAppBody{
		ProductID:   impl.option.ProductID,
		PodIDList:   []string{impl.option.DeviceID},
		PackageName: packageName,
	}
	_, err := impl.acep.LaunchApp(ctx, request)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) CloseApp(ctx context.Context, packageName string) error {
	request := &acep.CloseAppBody{
		ProductID:   impl.option.ProductID,
		PodIDList:   []string{impl.option.DeviceID},
		PackageName: packageName,
	}
	_, err := impl.acep.CloseApp(ctx, request)
	if err != nil {
		return err
	}
	return nil
}

func (impl *mobileUseImpl) ListApps(ctx context.Context) (appItems []AppItem, err error) {
	request := &acep.GetPodAppListQuery{
		ProductID: impl.option.ProductID,
		PodID:     impl.option.DeviceID,
	}

	response, err := impl.acep.GetPodAppList(ctx, request)
	if err != nil {
		return appItems, fmt.Errorf("GetPodAppList failed, error: %v", err)
	}
	if response == nil || len(response.Result.Row) == 0 {
		return appItems, fmt.Errorf("GetPodAppList failed, get empty app list")
	}
	for _, appItem := range response.Result.Row {
		app := AppItem{}
		if appItem.AppID != nil {
			app.AppID = *appItem.AppID
		}
		if appItem.AppName != nil {
			app.AppName = *appItem.AppName
		}
		if appItem.PackageName != nil {
			app.PackageName = *appItem.PackageName
		}
		if appItem.InstallStatus != nil && *appItem.InstallStatus == consts.ACEPAppInstallStatusSuccess {
			app.AppStatus = "deployed"
		} else {
			app.AppStatus = "undeployed"
		}
		appItems = append(appItems, app)
	}
	return appItems, nil
}

func (impl *mobileUseImpl) runSyncCommand(ctx context.Context, command string, user string) (*string, error) {
	request := &acep.RunSyncCommandBody{
		ProductID:      impl.option.ProductID,
		PodIDList:      []string{impl.option.DeviceID},
		Command:        command,
		PermissionType: &user,
	}
	response, err := impl.acep.RunSyncCommand(ctx, request)
	if err != nil {
		return nil, err
	}
	if response == nil || (response.ResponseMetadata.Error != nil && response.ResponseMetadata.Error.CodeN != 0) {
		return nil, fmt.Errorf("RunSyncCommand failed, error: %v", response.ResponseMetadata.Error)
	}
	if response.Result.ProductID != nil && *response.Result.ProductID != impl.option.ProductID {
		return nil, fmt.Errorf("RunSyncCommand failed, ProductID not match, expected: %s, actual: %s", impl.option.ProductID, *response.Result.ProductID)
	}
	if response.Result.Command != nil && *response.Result.Command != command {
		return nil, fmt.Errorf("RunSyncCommand failed, Command not match, expected: %s, actual: %s", command, *response.Result.Command)
	}
	if len(response.Result.Status) == 0 {
		return nil, fmt.Errorf("RunSyncCommand failed, Status is empty")
	}
	for _, status := range response.Result.Status {
		if status.PodID != nil && *status.PodID == impl.option.DeviceID {
			if status.Success != nil && *status.Success {
				return status.Detail, nil
			}
			return nil, fmt.Errorf("RunSyncCommand failed, Command failed, detail: %s", *status.Detail)
		}
	}
	return nil, fmt.Errorf("RunSyncCommand failed, Status not found")
}

func extractScreenshotURL(output string) (*ScreenShotResult, error) {
	// handle v1
	if strings.HasPrefix(output, "ScreenshotURL: ") {
		downloadUrl := strings.TrimPrefix(output, "ScreenshotURL: ")
		downloadUrl = strings.Trim(downloadUrl, "\n")
		if _, err := url.Parse(downloadUrl); err == nil {
			return &ScreenShotResult{
				ScreenshotURL: downloadUrl,
				Width:         0,
				Height:        0,
			}, nil
		}
	}

	// handle v2
	type phoneScreenshotResult struct {
		ScreenshotURL string `json:"screenshot_url"`
		Resolution    string `json:"resolution"`
	}
	var result phoneScreenshotResult
	if err := json.Unmarshal([]byte(output), &result); err != nil {
		return nil, fmt.Errorf("failed to parse screenshot result: %v, output: %s", err, output)
	}

	if result.ScreenshotURL == "" {
		return nil, fmt.Errorf("screenshot URL is empty")
	}
	if result.Resolution == "" {
		return nil, fmt.Errorf("screenshot resolution is empty")
	}

	if _, err := url.Parse(result.ScreenshotURL); err != nil {
		return nil, fmt.Errorf("invalid screenshot URL: %v", err)
	}

	width, height, err := parseResolution(result.Resolution)
	if err != nil {
		return nil, fmt.Errorf("invalid resolution format: %s, expected format: WIDTHxHEIGHT", result.Resolution)
	}

	return &ScreenShotResult{
		ScreenshotURL: result.ScreenshotURL,
		Width:         width,
		Height:        height,
	}, nil
}

func parseResolution(resolution string) (width, height int, err error) {
	parts := strings.Split(resolution, "x")
	if len(parts) != 2 {
		return 0, 0, fmt.Errorf("invalid resolution format")
	}

	width, err = strconv.Atoi(parts[0])
	if err != nil || width <= 0 {
		return 0, 0, fmt.Errorf("invalid width")
	}

	height, err = strconv.Atoi(parts[1])
	if err != nil || height <= 0 {
		return 0, 0, fmt.Errorf("invalid height")
	}

	return width, height, nil
}
