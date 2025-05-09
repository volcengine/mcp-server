package config

type MobileUseConfig struct {
	AuthInfo
	BizInfo
	TosInfo
}

type AuthInfo struct {
	CurrentTime     string
	ExpiredTime     string
	AccessKeyId     string
	SecretAccessKey string
	SessionToken    string
}

type BizInfo struct {
	ACEPHost  string
	ProductId string
	DeviceId  string
}

type TosInfo struct {
	TosBucket       string
	TosRegion       string
	TosEndpoint     string
	TosAccessKey    string
	TosSecretKey    string
	TosSessionToken string
}
