import uuid
import datetime

def saveBlogFile(parentPath, fileContent):
    today = datetime.date.today()
    tstr = today.strftime('%Y%m%d')
    randName = uuid.uuid1().hex
    fileName = tstr + '_' + randName
    with open(parentPath + fileName, 'w') as f:
        f.write(fileContent)
    return fileName