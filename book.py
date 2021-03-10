class Book():
    '''
    Это классс, предназначенный для хранения и представления информации отдельных текстов и их частей
    '''
    
    def __init__(self):
        
        self.chapters = []
        self.paragraphs = []
        self.words = []
        
        self.str_for_reg_ex = '([–\w\,\.\-\"\№\<\>\'\*\s\:\«\»\#\&\?\!\(\)\„\“\”\’\–\…\-\—\;\(\)\[\]]+)'
        
    def get_reg_ex(self, marker):
        s = ''.join([marker[0], self.str_for_reg_ex, marker[1]])
        return s
        
    def from_text(self, filename):
        f = open(filename, 'r')
        f.seek(0)
        self.data = f.read()
        f.close()

        #print(self.data[:1000])
        
        #self.data.decode()
        
        self.data = self.data.replace(u'\xa0', u' ')
        self.data = self.data.replace(u'\t', u' ')
        self.data = self.data.replace(u'„', u'«')
        self.data = self.data.replace(u'“', u'»')
        self.data = self.data.replace(u'\n\n', u'\n')
        self.data = self.data.replace(u'\n \n', u'\n')
        
        self.signs = self.get_signs(self.data)
        
    def get_structure(self, method='patterns'):
        if method == 'reg_ex':
            import re

            self.title = re.findall(self.get_reg_ex(['<titl>', '</titl>']), self.data)
            self.author = re.findall(self.get_reg_ex(['<auth>', '</auth>']), self.data)
            self.prefrace = re.findall(self.get_reg_ex(['<pref>', '</pref>']), self.data)
            self.chapters = re.findall(self.get_reg_ex(['<chpt>', '</chpt>']), self.data)
            self.chapters_names = re.findall(self.get_reg_ex(['<chpn>', '</chpn>']), self.data)
            self.epilogue = re.findall(self.get_reg_ex(['<epil>', '</epil>']), self.data)
        else:
            self.title = self.get_patterns(['<titl>', '</titl>'], self.data)
            self.author = self.get_patterns(['<auth>', '</auth>'], self.data)
            self.prefrace = self.get_patterns(['<pref>', '</pref>'], self.data)
            self.chapters = self.get_patterns(['<chpt>', '</chpt>'], self.data)
            self.chapters_names = self.get_patterns(['<chpn>', '</chpn>'], self.data)
            self.epilogue = self.get_patterns(['<epil>', '</epil>'], self.data)
        
        print(self.data.count('<chpt>'))
        sns = []
        for ch in self.chapters:
            a = self.get_signs(ch)
            sns.append(a)
            print(len(ch), ch[:100])
        
        #print(self.chapters[0])
        print("Считанных глав: ", len(self.chapters))
        print('Названных глав: ', len(self.chapters_names))
        print(self.chapters_names)
        
        s = ''
        for i in self.chapters:
            if i not in s:
                s += i
            
        new_signs = self.get_signs(s)
        print(new_signs)
        print(len(self.signs), len(new_signs))
        missed = []
        for ss in self.signs:
            if ss not in new_signs:
                missed.append(ss)
        
        print(self.signs)
        print('Пропущены: ', missed)
        
        self.tokens = s.split(' ')
        p = 0
        for t in self.tokens:
            if u'\t' in t:
                p +=1
                
    def get_patterns(self, tags, text):
        patterns = []
        a = tags[0]
        b = tags[1]

        s = ''
        tag = a
        end = ''
        for t in text:
            s += t
            len_tag = len(tag)
            if len(s) > len_tag:
                end = s[-len_tag:]
            #print(t, tag, len_tag, end, st)

            if end == a:
                s = ''
                tag = b
                end = ''
            if end == b:
                pattern = s[:-len(b)]
                patterns.append(pattern)
                s = ''
                tag = a
                end = ''
        return patterns
        
        
    def get_signs(self, text):
        signs = []
        for s in text:
            if s not in signs:
                signs.append(s)
        return signs
book.get_structure()
