import nonebot
from nonebot.log import logger, default_format
from nonebot.adapters.onebot.v11 import Adapter as V11Adapter


logger.add(
    "log/error.log",
    rotation="00:00",
    diagnose=False,
    level="ERROR",
    format=default_format,
)

nonebot.init()


driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)


nonebot.load_plugin("nonebot_plugin_alconna")
nonebot.load_plugin("nonebot_plugin_pong")
nonebot.load_plugin("nonebot_plugin_htmlrender")
# nonebot.load_plugin("nonebot_plugin_manager")

nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
