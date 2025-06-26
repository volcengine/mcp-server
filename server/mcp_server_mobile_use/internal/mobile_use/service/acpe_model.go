package service

type AppItem struct {
	AppID       string `json:"app_id"`
	AppName     string `json:"app_name"`
	AppStatus   string `json:"app_status"`
	PackageName string `json:"package_name"`
}

type TosConfig struct {
	AccessKey    string
	SecretKey    string
	SessionToken string
	Bucket       string
	Region       string
	Endpoint     string
}

type ScreenShotResult struct {
	ScreenshotURL string `json:"screenshot_url"`
	Width         int    `json:"width"`
	Height        int    `json:"height"`
}
