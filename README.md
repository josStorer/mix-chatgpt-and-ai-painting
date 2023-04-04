# Mix-ChatGPT-And-AI-Painting-And-Vits

[![license](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/josStorer/mix-chatgpt-and-ai-painting/blob/master/LICENSE)
[![qq](https://img.shields.io/badge/qq%E7%BE%A4-283430436-brightgreen.svg)](https://jq.qq.com/?_wv=1027&k=HwlnMCMr)
[![bilibili](https://img.shields.io/badge/bilibili-%E5%9B%BD%E6%9C%8D%E7%AC%AC%E4%B8%80%E6%B5%B7%E8%B1%B9-ff69b4.svg)](https://space.bilibili.com/8261016)

a bot application running on Tencent QQ that integrates GPT chatbot capabilities with AI painting.

一个运行于腾讯qq上的, 将gpt聊天能力与ai绘画集成的机器人应用.

Due to limited personal energy, currently this project is mainly aimed at Chinese users. If I have time in the
future, I may add more internationalization support. For English users, it should not be difficult to understand with
the help of variable names in the code. You can also translate this readme file into English to help you understand this
project. The core idea is to use prompts to guide the insertion of identifying text for the program to recognize and
execute instructions. Similar approaches can also be used for services such as voice services, group management, and
user image analysis. If this project can inspire or help you, I would be honored.

## Example

<div align=center>
<img src="screenshots/example1.png" width="400" alt="chat example"/>
</div>

## 常见问题

1. at机器人对话时, 本程序出现`AttributeError: 'Error' object has no attribute 'message'`
  - 一般是填写账号密码登陆openai的登陆错误, 如果你有代理, 请在[main.py#L95](https://github.com/josStorer/mix-chatgpt-and-ai-painting/blob/master/main.py#L95)
  邮箱密码后添加`"proxy": "你的代理地址"`, 如果你没有代理, 请将`use_chatgpt`设为`False`, 并填写`api_key`
2. 画图时, 机器人提示, `错误: 'images'`
  - 是Stable Diffusion WebUI没有暴露api, 你需要在启动时, 额外输入`--api`参数, 如果你使用的是他人的整合包, 请找到相关启动文件(一般是.bat后缀),
  找到其中有参数的一行, 如`--deepdanbooru`, `--xformers`, 在后面加上一个`--api`, 注意参数间空格

3. 如果出现了SSL Error，解决方案是卸载urllib3然后重装至1.25.11版本再重新运行一遍就可以。
  - 在终端或命令提示符中卸载urllib3
  pip uninstall urllib3

  - 然后，您可以通过使用指定版本号的pip install命令来安装所需的版本：
  pip install urllib3==1.25.11

如有使用问题, 可加qq群283430436交流, 也可进行试玩

4. Python版本安装3.10以内的版本,3.11在pip的时候会无法安装需要的依赖库.

5. 出现'Human:', 'AI:' 这样的回答模式，应该怎么处理？
  - 这种回答模式通常出现在Web版的使用中，需要使用`#清理对话`，防止对话模式继续污染下去。

6. 设置的人设不生效是为什么？
  - 要在`config.py`中，`use_chatgpt`和`billing_chatgpt`都设置为True，这样才会启用API模式
  - API模式支持系统级别的角色扮演，Web模式不支持
  - 设置gpt4人设会强制进入Web模式的对话，没有gpt3.5的账号使用gpt4可能也会成功，可能的原因是官方看你是gpt3.5的号就给你偷偷换成3.5的使用了。这里面有个风险，gpt3.5的号用web版越权申请使用gpt4，可能会被官方判风险操作导致账号被禁。

7. 能不能不输出文本，只输出语音？
  - 可以，`ws_wrapper.py`中的`send_record_to_group`函数最后一行`send_message_to_group`删掉

8. 如何获取bing-cookie？
  - 打开开发者模式，网络抓包点doc类型
  - 去bing.com
  - doc抓包第一个，找到request头里的cookie
  - 全复制过来，删掉中文项
  - 放到config的bing_cookie字符串中

## 食用方法

1. 下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases), 注意底部`show all ...`展开, windows一般使用windows_amd64.exe
2. 启动cmd窗口, 打开到go-cqhttp所在路径, 然后通过命令行输入程序名启动, 并选择正向websocket模式
3. 扫码登录你的qq机器人
4. 下载[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), 并安装依赖, 该项目也提供了不同系统的一键安装脚本,
   如果你是从源代码安装, 可参考https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running, 如果你下载的是他人的整合包, 可略过
5. 从huggingface下载模型权重,
   如[Anything](https://huggingface.co/andite/anything-v4.0/tree/main), [Chilloutmix](https://huggingface.co/TASUKU2023/Chilloutmix/tree/main), [OrangeMixs](https://huggingface.co/WarriorMama777/OrangeMixs/tree/main),
   放置在stable-diffusion-webui的`models/Stable-diffusion`目录下
6. 启动stable-diffusion-webui, 可以参考官方项目在不同系统的[启动说明](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running),
   也可参考[sd_webui.bat](sd_webui.bat), 如果所有依赖安装正常, 可以直接用webui.py启动, 如
   `python webui.py --medvram --deepdanbooru --xformers --api`, 注意必须带有`--api`参数, 如果你使用的是他人的整合包, 可能需要自己手动在启动脚本加上`--api`参数, 参考上面的`常见问题`一栏
7. 克隆本项目, `git clone https://github.com/josStorer/mix-chatgpt-and-ai-painting`, 并`pip install -r requirements.txt`
   安装依赖
8. 在本项目的[config.py](config.py)内修改属于你自己的配置,
   必须修改的变量为: `api_key`/`email,password`, `master_id`, `bot_id`,
   建议考虑实际情况修改的变量为: `use_chatgpt`, `working_groups`, `auth_vip_for_all`, `local_mode`, 其他请自行抉择
9. 使用`python main.py`启动本项目
10. 可选, 在本项目的几个.bat文件中, 正确配置你自己的路径, 然后设置开机启动[gpu_connect.bat](gpu_connect.bat),
    之后自己`win+tab`新建一个桌面干别的事情,
    让你的电脑闲置时给群友玩耍吧
11. 更多详细配置, 及服务器24小时在线模式, 查看[config.py](config.py)

## Vits语音版额外内容

1. 先把仓库clone下来，按照上面的步骤执行
2. 然后安装vits相关的依赖。
运行仓库根目录中的`安装.bat`文件
[FFmpeg依赖](https://github.com/BtbN/FFmpeg-Builds/releases/?spm=a2c6h.12873639.article-detail.4.55e41da65yk2qS)下载好之后添加`ffmpeg-master-latest-win64-gpl\bin`到操作系统的用户环境变量`%PATH%`中
3. 下载[錦木千束预训练语音模型](https://huggingface.co/spaces/yefengzi/vits-models/resolve/main/pretrained_models/chisato/chisato.pth) ，并放到`model/chisato`目录下命名为`chisato.pth`，能调通这个就行了
4. 此外，这个空间下还有刻晴和优拉的模型。分别对应`model/keqing/keqing.pth`、`model/eula/eula.pth`。
5. [派蒙预训练语音模型](https://mega.nz/file/4f0CgBaT#Hu4h_ZhVDC6V4RaS9zUeEJJY9cniqKx911z8duPSfCw) 对应`model/paimon/paimon.pth`
6. [Sayashi的804个语音模型](https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/G_953000.pth) 对应`model/804/804.pth`
7. proxy相关的参数，`127.0.0.1:XXXX`，后面的端口填自己本机的


## 指令一览

- 直接at机器人, 即可调用openai api进行对话, 在config.py内配置auth_vip_for_all=True授予所有人权限, 否则请使用vip指令
- #gpt切换: 在gpt3与chatgpt模式间切换
- #上线: 令该群聊的机器人上线, 使其允许执行openai调用和ai绘画
- #下线: 令该群聊的机器人下线, 使其不允许执行openai调用和ai绘画
- #画图: 令机器人在该群聊中画图, 例如: #画图 girl, 使用点或分号分隔, 允许一些快捷操作, 使用花括号允许传入细致的json配置操作,
  详细请使用 #帮助 查看
- #d: vip列表内的用户允许使用的快捷画图操作, 效果同 #画图
- #撤回: 撤回由你触发的上一条机器人消息
- #拉黑: 禁止该用户在该群聊中使用机器人
- #解除: 解除对该用户的拉黑
- #vip: 将该用户加入vip列表, vip列表内的用户可以使用 #d 指令, 也可以通过at调用机器人, 执行openai api对话
- #unvip: 将该用户从vip列表中移除
- #清理对话: 清理对话上下文(先前对话内容过长导致请求失败时, 可以选择清理)
- #帮助: 显示面向群内普通用户的帮助信息, 不含vip指令和master指令
- #默认: 显示 #画图 的默认json配置, 你可以直接复制这些信息自己修改, 然后再通过 #画图 {...} 传回去调用
- #黑名单: 显示黑名单列表
- #at切换: 切换机器人响应模式, 默认总是需要at机器人以进行openai回复, 切换后可以直接对话, 对每句话都进行回复

## 文件功能说明

- main.py: 程序入口, 使用python main.py启动
- config.py: 根据你自己的情况进行调整的配置文件, 基本每一项都有注释, 直接查看即可
- operations.py: 各项指令功能, 文件底部有一个字典变量存储了所有指令及对应函数调用, 仿照扩展即可
- requirements.txt: 依赖列表, 使用pip install -r requirements.txt安装
- global_var: 全局变量
- utils.py: 一些工具函数
- ws_wrapper.py: 封装了一些websocket消息, 用于和go-cqhttp通信
- gpu_connect.bat: 用于快捷启动各关联程序, 请自行修改路径
- sd_webui.bat: 快捷启动stable-diffusion-webui
- cqhttp.bat: 快捷启动go-cqhttp

修改main.py内的on_message函数, 及ws_wrapper.py, 以尝试为QQ以外的其他程序开发机器人应用

## 附注

这个项目一开始只是给沙雕群友们搞的玩具, 图一乐来着, 最近搞真人模型的时候, 顺便集成了gpt对话功能, 感觉效果还不错, 就开源了

核心思路看config.py的prompt就懂了, 类似思路, 也可用于生成语音对话, 管理群聊等, 仅作抛砖引玉, 欢迎大伙fork改造

代码和git日志很拉, 因为一开始就是个玩具项目, 直接一把梭做出来的, 而且记录里还有我自己的域名和key等隐私信息, 所以直接新建了一个项目,
没有log了

<img src="screenshots/bad_log.png" width="600" alt="bad log"/>
