import pykakasi
 
def convert_to_romaji(text):
    """
    漢字仮名混じり文をローマ字に変換する
 
    Parameters
    ----------
    text : str
        ローマ字に変換したい漢字仮名交じり文
 
    Returns
    -------
    result : str
        ローマ字に変換した文字列
 
    Notes
    -------
    下記サイトを参考に作成しました
    https://github.com/miurahr/pykakasi  
    """
 
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")        # Hiragana to ascii
    kakasi.setMode("K", "a")        # Katakana to ascii
    kakasi.setMode("J", "a")        # Japanese to ascii
    kakasi.setMode("r", "Hepburn")  # use Hepburn Roman table
    kakasi.setMode("s", False)       # add space
    kakasi.setMode("C", False)      # no capitalize
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result