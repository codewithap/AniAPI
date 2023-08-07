from utils import useragent
from scrappers import gogoscrapper
import time



t = time.time()
print(gogoscrapper().getEpis("naruto")[1])
print(time.time() - t)
# print(useragent())


