from opencc import OpenCC

cc = OpenCC('t2s')

def converter(text: str) -> str:
  return cc.convert(text)

def traditional_to_simplified_chinese(texts: str | list[str]) -> str | list[str]:
  if type(texts) is list:
    return [converter(x) for x in texts]
  else:
    return converter(texts)
