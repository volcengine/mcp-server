note = {
    "start_voice_chat": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
           #{.custom-md-table-4}#
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            AppId ( String ): 是  你的音视频应用的唯一标志，参看创建 RTC 应用获取或创建 AppId。 
            RoomId ( String ): 是  智能体与真人进行通话的房间的 ID，需与真人用户使用客户端 SDK 进房时的使用的 RoomId 保持一致。 
            TaskId ( String ): 是  智能体任务 ID。由你自行定义，用于标识任务，且后续更新或结束此任务也需要使用该 TaskId。参数定义规则参看参数赋值规范。 
                  - 一个 AppId 的 RoomId 下 TaskId 是唯一的，AppId + RoomId + TaskId 共同构成一个全局唯一的任务标识，用来标识指定 AppId 下某个房间内正在运行的任务，从而能在此任务运行中进行更新或者停止此任务。 
                  - 不同 AppId 或者不同 RoomId 下 TaskId 可以重复。 
            Config ( Object of Config ): 是  智能体交互服务配置，包括语音识别（ASR）、语音合成（TTS）、大模型(LLM)、字幕和函数调用（Function Calling）配置。 
            AgentConfig ( Object of AgentConfig ): 是  智能体相关配置，包括欢迎词、任务状态回调等信息。 
           #{.custom-md-table-4}#
           "字段"： Config
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ASRConfig ( Object of ASRConfig ): 是  语音识别（ASR）相关配置。 
            TTSConfig ( Object of TTSConfig ): 是  语音合成（TTS）相关配置。 
            LLMConfig ( Object ): 是  大模型相关配置。支持的大模型平台如下： 
                  - 火山方舟平台 
                  - Coze平台 
                  - 第三方大模型/Agent 
            SubtitleConfig ( Object of SubtitleConfig ): 否  配置字幕回调。 
                  可通过客户端或服务端接收回调消息，消息格式为二进制，使用前需解析。详细说明参看实时对话式 AI 字幕。 
            FunctionCallingConfig ( Object of FunctionCallingConfig ): 否  使用 Function calling 功能时，从服务端接受函数工具返回的信息指令配置。 
                  Function calling  功能使用详情参看功能说明文档。 
                  - - 该功能仅在使用火山方舟平台时生效，且对模型有限制。具体请参见功能说明文档。 
                  - ServerMessageUrl 和 ServerMessageSignature 均填写正确才能开启 Function calling 功能。 
            InterruptMode ( Integer ): 否  是否启用语音打断（发声即打断）： 
                  - 0：开启。开启后，一旦检测到用户发出声音，智能体立刻停止输出。 
                  - 1：关闭。关闭后，智能体说话期间，用户语音输入内容会被忽略不做处理，不会打断智能体讲话。 
                  默认值为 0。 
            AvatarConfig ( Object of AvatarConfig ): 否   
           #{.custom-md-table-4}#
           "字段"：# ASRConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Provider ( String ): 是  语音识别服务的提供商： 
                  - volcano：火山引擎语音识别服务。可使用以下模型： 
                  	- 火山引擎流式语音识别（识别速度更快） 
                  	- 火山引擎流式语音识别大模型（识别准确率更高） 
                    两者详细差异（如可识别语种、支持的能力等），请参见流式语音识别和流式语音识别大模型。 
                  - ai_gateway：自定义语音合成模型（通过火山边缘大模型网关接入的） 
            ProviderParams ( Object ): 是  服务配置参数。不同服务，ProviderParams 包含的字段不同： 
                  - 火山引擎流式语音识别 
                  - 火山引擎流式语音识别大模型 
                  - 自定义语音识别 
            VADConfig ( Object of VADConfig ): 否  VAD（语音检测） 配置。 
            VolumeGain ( Float ): 否  音量增益值。增益值越低，采集音量越低。适当低增益值可减少噪音引起的 ASR 错误识别。 
                  默认值为 1.0，推荐值 0.3。 
            InterruptConfig ( Object of InterruptConfig ): 否  语音打断配置，支持：基于说话时长打断、关键词打断。 
            TurnDetectionMode ( Integer ): 否  新一轮对话的触发方式。 
                  - 0：服务端检测到完整的一句话后，自动触发新一轮对话。 
                  - 1：收到输入结束信令或说话字幕结果后，你自行决定是否触发新一轮会话。 
                  默认值为 0。 
                  该功能使用方法参看配置对话触发模式。 
           #{.custom-md-table-4}#
           `mixin-react
           const TabsPane_0 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_1 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_2 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           return (
           )
           `
           "字段"：## VADConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            SilenceTime ( Integer ): 否  判停时间。房间内真人用户停顿时间若高于该值设定时间，则认为一句话结束。 
                  取值范围为 [500，3000)，单位为 ms，默认值为 600。 
            AIVAD ( Boolean ): 否  是否开启智能语义断句： 
                  - true：开启。启用后系统会结合 AI 模型对语义完整性的判断和 SilenceTime 来进行断句，能更准确地处理长句中的自然停顿，有效避免将一句话错误切分。 
                  - false（默认值）：关闭。 
                  AIVAD 功能目前在限时免费公测阶段。 
           #{.custom-md-table-4}#
           "字段"：## InterruptConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InterruptSpeechDuration ( Integer ): 否  自动打断的触发阈值，即真人用户持续说话时间达到设定值，智能体才自动停止输出。 
                  - 取值范围：0 或 [200，3000]，单位为 ms。值越大，智能体越不容易被打断。 
                  - 默认值：0，表示用户发出声音且包含真实语义时，即打断智能体输出。 
            InterruptKeywords ( Array of String ): 否  触发打断的关键词列表。当用户语音中识别到列表中的任意关键词时，智能体将立即停止输出。 
                  若配置该参数，只有识别到配置的打断词时才会触发打断，以降低背景环境人声无打断的干扰。使用该参数时，建议 InterruptSpeechDuration 设置为 0，避免自动打断触发阈值过高，导致关键词打断不生效。 
           #{.custom-md-table-4}#
           "字段"：# TTSConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            IgnoreBracketText ( Array of Integer ): 否  过滤大模型返回内容中指定标点符号中的文字后再进行语音合成。你需要在大模型 Prompt 中自行定义哪些内容放在指定标点符号内。具体使用方法参看过滤指定内容。 
                  支持取值及含义如下： 
                  - 1：中文括号（） 
                  - 2：英文括号() 
                  - 3：中文方括号【】 
                  - 4：英文方括号[] 
                  - 5：英文花括号{} 
                  默认值为空，表示不进行过滤。 
                  若大模型返回的内容中，包含标点符号里的内容在最末端，且为独立句子，其后无包含真实语义内容，该标点符号中的内容不会出现在字幕中。 
                  - 示例 1：如大模型返回的内容为：当然可以，尽管问，我知无不言！(自信满满)。， 
                  此时（自信满满）。不会出现在字幕里。 
                  - 示例 2：如大模型返回的内容为：当然可以，尽管问，我知无不言(自信满满)！， 
                  此时（自信满满）会出现在字幕里。 
            Provider ( String ): 是  语音合成服务提供商，使用不同语音合成服务时，取值不同。支持使用的语音合成服务及对应取值如下： 
                  - volcano（服务自上而下语音生成速度递减，情感表现力递增） 
                  	- 火山引擎语音合成 
                  	- 火山引擎语音合成大模型（非流式输入流式输出） 
                    - 火山引擎声音复刻大模型（非流式输入流式输出） 
                  - volcano_bidirection（服务自上而下语音生成速度递减，情感表现力递增） 
                  	- 火山引擎语音合成大模型（流式输入流式输出） 
                    - 火山引擎声音复刻大模型（流式输入流式输出） 
                  - minimax：MiniMax 语音合成 
                  - ai_gateway：自定义语音合成模型（通过火山边缘大模型网关接入的） 
            ProviderParams ( Object ): 是  配置所选的语音合成服务。不同服务下，该结构包含字段不同： 
                  - 火山引擎语音合成 
                  - 火山引擎语音合成大模型（非流式输入流式输出） 
                  - 火山引擎语音合成大模型（流式输入流式输出） 
                  - 火山引擎声音复刻大模型（非流式输入流式输出） 
                  - 火山引擎声音复刻大模型（流式输入流式输出） 
                  - MiniMax 语音合成 
                  - 自定义语音合成 
           #{.custom-md-table-4}#
           `mixin-react
           const TabsPane_0 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_1 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_2 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_3 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_4 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_5 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_6 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           return (
           )
           `
           `mixin-react
           const TabsPane_0 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_1 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           const TabsPane_2 = () => {
           const columns = undefined;
           const data = undefined
           return undefined
           }
           return (
           )
           `
           "字段"：# SubtitleConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            DisableRTSSubtitle ( Boolean ): 否  是否关闭房间内客户端字幕回调。 
                  - true：关闭，即不通过客户端接收字幕回调消息。 
                  - false：开启，通过客户端接收字幕回调消息。开启后，在客户端实现监听 onRoomBinaryMessageReceived（以 Android 为例），即可接收字幕回调消息。 
                  默认值为 false。 
                  如需通过服务端接收字幕回调，请配置 ServerMessageUrl 和 ServerMessageSignature。 
            ServerMessageUrl ( String ): 否  接收字幕结果的 URL 地址。通过服务端接收字幕回调时必填。 
                  接收结果的 URL 必须以域名开头。如果 URL 为 HTTPS 域名，请确保该域名 SSL 证书合法且完整。 
                  你可通过 curl -v http(s)://yourexample-domain.com/vertc/subtitle 命令对域名进行快速校验： 
                  - 失败场景： 
                  	- 返回 301 或 302，说明域名不可用，POST 方法可能会重定向为 GET。 
                  	- 使用 HTTP 域名时，可能导致返回 302，出现该情况时建议改为 HTTPS 域名。 
                  - 成功场景：若返回 307 或 308 则说明域名可用，且始终保持 POST 方法。 
                  如果你同时通过该接口接收任务状态变化回调和字幕回调，请确保在 ServerMessageUrl 和 ServerMessageURLForRTS 中填入相同的 URL，否则会导致无法接收任务状态回调或字幕回调。 
            ServerMessageSignature ( String ): 否  鉴权签名。通过服务端接收字幕回调时必填。 
                  在接收到字幕结果后，与结果中的 signature 字段值进行对比以进行鉴权验证。 
            SubtitleMode ( Integer ): 否  字幕回调时是否需要对齐音频时间戳。 
                  - 0：对齐音频时间戳。 
                  - 1：不对齐音频时间戳。取 1 时可更快回调字幕信息。 
                  默认值为 0。 
           #{.custom-md-table-4}#
           "字段"：# FunctionCallingConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ServerMessageUrl ( String ): 否  服务端接收 Function Calling 函数工具返回的信息指令的 URL 地址。功能使用详情参看服务端实现 Function Calling 功能。 
                  URL 必须以域名开头。如果 URL 为 HTTPS 域名，请确保该域名 SSL 证书合法且完整。 
                  - 失败场景： 
                  	- 返回 301 或 302，说明域名不可用，POST 方法可能会重定向为 GET。 
                  	- 使用 HTTP 域名时，可能导致返回 302，出现该情况时建议改为 HTTPS 域名。 
                  - 成功场景：若返回 307 或 308 则说明域名可用，且始终保持 POST 方法。 
            ServerMessageSignature ( String ): 否  鉴权签名。 
                  在接收到函数调用信息结果后，与结果中的 signature 字段值进行对比以进行鉴权验证。 
           #{.custom-md-table-4}#
           "字段"：# AvatarConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Enabled ( Boolean ): 是  是否开启数字人；默认值：False 
            AvatarAppID ( String ): 是  数字人服务AppID 
            AvatarToken ( String ): 是  数字人服务Token 
            AvatarType ( String ): 是  数字人类型 
                  - pic: 单图数字人 
                  - 3min: 3min克隆数字人 
            AvatarRole ( String ): 是  数字人角色ID 
            BackgroundUrl ( String ): 否  数字人背景图URL, 需要带有图片格式后缀，如 .png .jpg. 
                  （仅AvatarType=3min时支持背景图） 
            VideoBitrate ( Integer ): 否  数字人视频码率, 单位为 kbps，取值范围 [100, 8000] 
           #{.custom-md-table-4}#
           "字段"： AgentConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            TargetUserId ( Array of String ): 是  真人用户 ID。需使用客户端 SDK 进房的真人用户的 UserId。仅支持传入一个 UserId，即单个房间内，仅支持一个用户与智能体一对一通话。 
            WelcomeMessage ( String ): 否  智能体启动后的欢迎词。 
            UserId ( String ): 否  智能体 ID，用于标识智能体。 
                  由你自行定义、生成与维护，支持由大小写字母（A-Z、a-z）、数字（0-9）、下划线（_）、短横线（-）、句点（.）和 @ 组成，最大长度为 128 个字符。 
                  若不填则默认值为 voiceChat_$(TargetUserId)_$(timestamp_now)。 
                  - 同一 AppId 下 UserId 建议全局唯一。若同一 AppId 下不同房间内智能体名称相同，会导致使用服务端回调的功能异常，如字幕、Function Calling 和任务状态回调功能。 
                  - UserId 取值与 TargetUserId 不能重复。 
            EnableConversationStateCallback ( Boolean ): 否  是否接收智能体状态变化回调，获取智能体关键状态，比如     
                  “聆听中”、“思考中”、“说话中”、“被打断”等。功能详细说明，参看接收状态变化消息。 
                  - true：接收。可通过客户端或服务端接收智能体状态变化回调。 
                  	- 通过客户端接收：还需在客户端实现监听回调 onRoomBinaryMessageReceived（以 Android 端为例）。 
                  	- 通过服务端接收：还需配置字段 ServerMessageURLForRTS 和 ServerMessageSignatureForRTS。 
                  - false：不接收。 
                  默认值为 false。 
            ServerMessageSignatureForRTS ( String ): 否  鉴权签名。通过服务端接受任务状态变化回调时必填。 
                  你可传入该鉴权参数，在接收到回调结果后，与结果中的 signature 字段值进行对比以进行鉴权验证。 
            ServerMessageURLForRTS ( String ): 否  接收任务状态变化的 URL 地址。通过服务端接受任务状态变化回调时必填。 
                  接收结果的 URL 必须以域名开头。如果 URL 为 HTTPS 域名，请确保该域名 SSL 证书合法且完整。  
                  - 失败场景： 
                  	- 返回 301 或 302，说明域名不可用，POST 方法可能会重定向为 GET。 
                  	- 使用 HTTP 域名时，可能导致返回 302，出现该情况时建议改为 HTTPS 域名。 
                  - 成功场景：返回 307 或 308，说明域名可用，且始终保持 POST 方法。 
                  如果同时通过该接口接收任务状态变化回调和字幕回调，请确保在 ServerMessageURLForRTS 与 SubtitleConfig.ServerMessageUrl 中填入相同的 URL，否则会导致无法接收任务状态回调或字幕回调。 
            UseLicense ( Boolean ): 否  是否为 License 用户。 
                  - true：是。 
                  - false：否。 
                  默认值为 false。 
                  若为 License 用户，你需要： 
                  1. 联系技术支持开通白名单。 
                  2. 前往控制台硬件场景服务获取你需要的 ASR、TTS 和 LLM 相关参数值。注意你必须使用在此处获取的 ASR、TTS 和 LLM 参数值，智能体才能正常工作。 
                  3. 如果你使用大模型流式语音识别和大模型语音合成，在调用 StartVoiceChat 接口时，ASRConfig.ProviderParams.AccessToken 和 TTSConfig.ProviderParams.AccessToken 无需填入。 
            Burst ( Object of Burst ): 否  音频快速发送配置。 
                  开启该功能后，可通过快速发送音频实现更快更好的抗弱网能力。 
                  该功能仅在嵌入式硬件场景下支持，且嵌入式 Linux SDK 版本不低于 1.57。 
            IdleTimeout ( Integer ): 否  当智能体已入房，真人用户（TargetUserID）持续不在房时，智能体的最长等待时间。超过该时间，智能体任务将自动停止并退出房间。 
                  - 单位：秒。 
                  - 默认值：180s。 
                  - 取值范围：大于 0 的整数。 
            AnsMode ( Integer ): 否  AI 降噪。对音频进行智能降噪处理，适用于不具备或不便开启端上 AI 降噪能力的终端。例如：若物联网、智能硬件设备算力有限，无法运行复杂的端上降噪算法的场景。 
                  可根据实际噪声环境选择不同级别的降噪模式： 
                  - 0（默认值）：禁用 AI 降噪。 
                  - 1：轻度降噪。适用于抑制微弱、平稳的背景噪声。 
                  - 2：中度降噪。适用于抑制中度平稳噪声，如空调声、风扇声。 
                  - 3：强度降噪。适用于抑制嘈杂、非平稳的动态噪音，如键盘敲击声、物体碰撞声、动物叫声等。 
            VoicePrint ( Object of VoicePrint ): 否  声纹降噪配置。可用于提升在多人环境下的语音识别准确率。 
                  启用后，系统将识别人声并保留目标用户（TargetUserID）的声纹，同时抑制环境中的其他无关人声（旁人噪音）。 
                  - 声纹降噪功能目前为免费公测阶段，算法还在进一步优化。 
                  - 开启声纹降噪时，建议不要开启 AI 降噪，以免影响声纹降噪效果。 
           #{.custom-md-table-4}#
           "字段"：# Burst
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Enable ( Boolean ): 否  是否开启音频快速发送。 
                  - false：关闭。 
                  - true：开启。 
                  默认值为 false。 
            BufferSize ( Integer ): 否  接收音频快速发送片段时，客户端可缓存的最大音频时长。取值范围为[10, 3600000]，单位为 ms，默认值为 10。 
            Interval ( Integer ): 否  音频快速发送结束后，其他音频内容发送间隔。 [10, 600]，单位为 ms，默认值为 10。 
           #{.custom-md-table-4}#
           "字段"：# VoicePrint
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Mode ( Integer ): 否  声纹降噪模式。 
                  - 0（默认值）： 
                  - 1：开启声纹降噪。 
            IdList ( Array of String ): 否  声纹 ID 列表。支持以下传参方式： 
                  - 传入 1 个已注册声纹 ID：系统会加载指定的声纹，并仅保留与该声纹匹配的人声。仅支持传入 1 个声纹 ID。 
                    > 你可以调用接口 RegisterVoicePrint 和 ListVoicePrint 为目标用户注册声纹或获取已注册声纹 ID（对应字段 VoicePrintId）。 
                    > 注意：注册声纹使用的音频，其采集设备需要和客户真实通话时使用的音频采集设备保持一致，以保证最佳效果。 
                  - 不传：则实时生成声纹。系统会在通话开始时，自动学习当前目标用户（TargetUserID）的声音特征。当用户累计说话时长达到30秒后，系统会生成一个临时声纹，用于本次通话的降噪。注意：在累计满 30 秒前，声纹降噪不会生效。 
           #{.custom-md-table-4}#
    """,
    "update_voice_chat": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
           #{.custom-md-table-4}#
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            AppId ( String ): 是  你的音视频应用的唯一标志，参看创建 RTC 应用获取或创建 AppId。 
            RoomId ( String ): 是  真人与 AI 会话的 RTC 房间 ID。 
            TaskId ( String ): 是  已发起的智能体任务 ID。需与 StartVoiceChat 配置的一致。 
            Command ( String ): 是  要执行的指令。不同的指令对应不同的功能，并决定了其他参数（如 Message）是否需要填写。 
                  - interrupt：打断智能体。使用方法参见手动打断。 
                  - function：向 LLM 回传 Function Calling 的工具调用结果。使用方法参见Function Calling。 
                  - ExternalTextToSpeech ： 传入文本信息让智能体主动播报。使用方法参看自定义语音播放。 
                  - ExternalPromptsForLLM：传入自定义文本作为背景信息，与用户的下一轮语音输入拼接后一同送入 LLM。使用方法参见提供背景信息（不立即回复）。 
                  - ExternalTextToLLM：传入外部文本作为当前轮次的用户输入，直接送入 LLM 进行提问。当与 ImageConfig 参数一同使用时，可实现外部图片和文本的同步输入。使用方法参看通过文本直接提问和外部图片理解。 
                  - FinishSpeechRecognition：触发新一轮对话。 
            Message ( String ): 否  指令关联的消息内容。 
                  该字段是否必填以及其内容格式，取决于 Command 字段的值： 
                  - 仅当 Command 为以下值时，Message 为必填：function、ExternalTextToSpeech、ExternalPromptsForLLM 或 ExternalTextToLLM。对于其他 Command 值，此字段应忽略。 
                  - 内容格式要求： 
                  	- 当 Command 值为 function 时，Message 格式需为 JSON 转译字符串，例如： 
                  "{"ToolCallID":"call_cx","Content":"上海天气是台风"}"。 
                    - Command 为其他值时：格式为普通字符串，例如"你刚才的故事讲的真棒。" 
                  - 内容长度要求：当 Command 值为 ExternalTextToSpeech 时，Message 传入内容建议不超过 200 个字符。 
            InterruptMode ( Integer ): 否  传入文本信息或外部问题时，处理的优先级。 
                  - 1：高优先级。传入信息直接打断交互，进行处理。 
                  - 2：中优先级。等待当前交互结束后，进行处理。 
                  - 3：低优先级。如当前正在发生交互，直接丢弃 Message 传入的信息。 
                  仅当 command 为 ExternalTextToSpeech 或 ExternalTextToLLM 时为该参数为必填。 
            ImageConfig ( Object of ImageConfig ): 否  用于向具备视觉能力的 LLM 传入图片进行理解。 
                  此参数仅在 Command 为 ExternalTextToLLM 时生效。 
           #{.custom-md-table-4}#
           "字段"： ImageConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
                  - insert：插入图片。系统会缓存传入的图片。 
                  - delete：删除指定 GroupID 的缓存图片。 
            GroupID ( Integer ): 是  图片轮次 ID。 
                  - Action 为 inset 时：用于关联同一轮对话中的图片和文本。该 ID 由您自定义和维护，需保证 ID 单调递增。 
                  - Action 为 delete 时：使用 GroupID 来清理系统缓存的图片。 
            ImageType ( String ): 否  要传入的图片的数据类型。目前固定为 url。 
                  当 Action 为 insert 时为必填。 
            Images ( String ): 否  指定要传入的图片 URL 地址，需确保 URL 地址可被公网访问。 
                  当 Action 为 insert 时为必填。 
           #{.custom-md-table-4}#
    """,
    "stop_voice_chat": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
           #{.custom-md-table-4}#
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            AppId ( String ): 是  你的音视频应用的唯一标志，参看创建 RTC 应用获取或创建 AppId。 
            RoomId ( String ): 是  真人与 AI 会话的 RTC 房间 ID。 
            TaskId ( String ): 是  智能体任务 ID 
           #{.custom-md-table-4}#
    """,
}
