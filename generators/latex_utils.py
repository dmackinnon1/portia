class LFigure:
    def __init__(self, caption, label):
        self.c = caption
        self.l = label
    def diagram(self, tab):
        self.t = tab
    def build(self):
        result ="%GENERATED CODE - DO NOT MODIFY\n"
        result = result + "\\begin{figure}[!htbp]\n"
        result = result +"\\caption{" + self.c + "}\n"
        result = result + self.t.build()
        result = result +"\\vspace{10pt}\n"
        result = result +"\\label{" + self.l + "}\n"
        result = result +"\\end{figure}\n"
        return result


class LType(object):
    def __init__(self):
        self.comments = []
    def addComment(self, comment):
        self.comments.append(comment)
        return self

class LRow:
    def __init__(self, size):
        self.length = size
        self.entries = []
    def add(self, e):
        self.entries.append(e)
        return self
    def build(self):
        result = ""
        counter = 0
        self.length = len(self.entries)
        for x in self.entries:
            counter = counter +1
            result = result + str(x)
            if (counter < self.length):
                result = result +" & "
            else:
                result = result + "\\\\"
        result = result + '\n'
        return result
    def addAll(self, bunch):
        for x in bunch:
            self.add(x)
        return self

class MRule:
    def build(self):
        return "\\midrule\n"

class MultiCol:
    def __init__(self,cols,align,text):
        self.result = "\\multicol{"+str(cols)+"}{"+align+"}{"+text+"}\\\\" +"\n"

    def build(self):
        return self.result

class MultiRow:
    def __init__(self,rows,text):
        self.result = "\\multirow{"+str(rows)+"}{*}{"+text+"} "

    def build(self):
        return self.result

class LTabular (LType):
    def __init__(self,cols):
        self.columns = cols
        self.rows = []
        super(LTabular,self).__init__()

    def add(self, r):
        self.rows.append(r)
        return self

    def build(self):
        result = "% GENERATED CODE: DO NOT MODIFY \n"
        for x in self.comments:
            result = result + "% " + x + "\n"

        result = result + "\\begin{tabular}{" + self.columns + "}\n"
        result = result + "\\toprule\n"
        for x in self.rows:
            result = result + x.build()
        result = result + "\\bottomrule\n\\end{tabular}"
        return result

class LBox: # for resizing if required
    def __init__(self, contents):
        self.c = contents
        self.m = str(1)

    def mult(self,m):
        self.m = str(m)

    def build(self):
        result = "\\resizebox{"+ self.m + "\\linewidth}{!}{\n"
        result = result + self.c.build()
        result = result +"\n}"
        return result

class LThreePart (LType):
    def __init__(self, tabular):
        self.notes=[]
        self.t = tabular
        super(LThreePart,self).__init__()

    def addNote(self, n):
        self.notes.append(n)
        return self

    def build(self):
        result = "% GENERATED CODE: DO NOT MODIFY \n"
        for x in self.comments:
            result = result + "% " + x + "\n"
        result += "\\begin{threeparttable}\n"
        result = result + self.t.build()

        if (len(self.notes) > 0):
            result = result +"\n\\vspace{10pt}"
            result = result +"\n\\begin{tablenotes}\n"
            result = result +"\\footnotesize\n"
            for n in self.notes:
                result = result + "\\item "+n +"\n"
            result = result + "\\end{tablenotes}\n"

        result = result +"\\end{threeparttable}\n"
        return result


class LTable (LType):
    def __init__(self, caption, label):
        self.c = caption
        self.l = label
        self.notes = []
        super(LTable,self).__init__()

    def tabular(self, tab):
        self.t = tab

    def build(self):
        result = "% GENERATED CODE: DO NOT MODIFY \n"
        for x in self.comments:
            result = result + "% " + x + "\n"

        result = result + "\\begin{table}[!htbp]\n"
        result = result +"\\caption{" + self.c + "}\n"
        result = result +"\\label{" + self.l + "}\n"
        result = result + self.t.build()
        result = result +"\\end{table}\n"
        return result
