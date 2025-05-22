package service

type mobileUseOption struct {
	AccessKey       string
	SecretKey       string
	SessionToken    string
	Host            string
	ProductID       string
	DeviceID        string
	Bucket          string
	Region          string
	Endpoint        string
	TosAccessKey    string
	TosSecretKey    string
	TosSessionToken string
}

type Option func(*mobileUseOption)

func defaultMobileUseOption() *mobileUseOption {
	return &mobileUseOption{
		AccessKey:    "",
		SecretKey:    "",
		SessionToken: "",
		Host:         "open.volcengineapi.com",
	}
}

func WithAccessKey(accessKey string) Option {
	return func(option *mobileUseOption) {
		option.AccessKey = accessKey
	}
}

func WithSecretKey(secretKey string) Option {
	return func(option *mobileUseOption) {
		option.SecretKey = secretKey
	}
}

func WithSessionToken(sessionToken string) Option {
	return func(option *mobileUseOption) {
		option.SessionToken = sessionToken
	}
}

func WithHost(host string) Option {
	return func(option *mobileUseOption) {
		option.Host = host
	}
}

func WithProductID(productID string) Option {
	return func(option *mobileUseOption) {
		option.ProductID = productID
	}
}

func WithDeviceID(deviceID string) Option {
	return func(option *mobileUseOption) {
		option.DeviceID = deviceID
	}
}

func WithBucket(bucket string) Option {
	return func(option *mobileUseOption) {
		option.Bucket = bucket
	}
}

func WithRegion(region string) Option {
	return func(option *mobileUseOption) {
		option.Region = region
	}
}

func WithEndpoint(endpoint string) Option {
	return func(option *mobileUseOption) {
		option.Endpoint = endpoint
	}
}

func WithTosAccessKey(accessKey string) Option {
	return func(option *mobileUseOption) {
		option.TosAccessKey = accessKey
	}
}

func WithTosSecretKey(secretKey string) Option {
	return func(option *mobileUseOption) {
		option.TosSecretKey = secretKey
	}
}

func WithTosSessionToken(sessionToken string) Option {
	return func(option *mobileUseOption) {
		option.TosSessionToken = sessionToken
	}
}
