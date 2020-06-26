# coding: utf-8

import codecs
import cStringIO
import csv

#UnicodeWriter from http://docs.python.org/2/library/csv.html#examples
class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

#/end UnicodeWriter

resultFile = open("relations"+timestamp+".csv",'wb')
wr = UnicodeWriter(resultFile,dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(['.'])

rtotal = 0

for term in allconcepts:
    rts = getrelatedterms(term)
    if rts == None:
        pass
    else:
        for rt in rts:
            wr.writerow([lit(term)]+["is related to"]+[lit(rt)])
            rtotal+=1


resultFile.close()
print 'finished listing all related concept connections, total: '+str(rtotal)