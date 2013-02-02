import re

class Parser():
    def __init__(self):
        self.NodeIndex = 0  ##Def any frame to a Node,and to point the SEQ,it is need a index
        self.Background =None
        self.BGM = None
        self.Name = ''  ##The argv about the speaker's name,maybe who is NONE
        self.Text = ''
        self.ChoiceBranch = []
        self.Portrait = {}

        self.RPIndex = self.__InitReParserIndex()
        self.RPBackground = self.__InitReParserBackground()
        self.RPBGM = self.__InitReParserBGM()            
        self.RPText = self.__InitReParserText()

        self.RPChoice = self.__InitReParserChoice()
        self.RPPortrait = self.__InitReParserPortrait()
        ##There of above are REGULAR EXPRESSION,to paser the Gammer which I define
        ##only ONE compile can cut some time,MAYBE.....

    def __InitReParserIndex(self):
        pat = r'^\d+?$' 
        ##TELL re to match any line
        return re.compile(pat,re.M)
    
    def __InitReParserBackground(self):
        pat = r'''^\[background\s*?=\s*?'(.+?)'\]$'''
        return re.compile(pat,re.M)

    ## I think paser a gammer like [BGM=xxx] is a good way
    def __InitReParserBGM(self): 
        pat = r'''^\[BGM\s*?=\s*?'(.+?)'\]$'''
        return re.compile(pat,re.M)

    ##I'd to use THE spcial way to define TEXT,like this:<TEXT>
    def __InitReParserText(self):
        pat = r'\<(.+?)\>'
        ##TELL re to match \n
        return re.compile(pat,re.DOTALL)

    def __InitReParserPortrait(self):
        pat = r'\{(.*?)\}'
        return re.compile(pat,re.DOTALL)
   
    def __InitReParserChoice(self):
        pat = r'(.+?)->(\d+)'
        return re.compile(pat)
    
    ##split the script by each empty line
    def split(self,target):
        script = open(target)
        LNode = []
        Node = ''
        for line in script:
            if line != '\n':
                Node += line
            else:
                LNode.append(Node)
                Node = ''
        LNode.append(Node)
        return LNode
        
    def parser(self,target):
        if not self.RPIndex.search(target):
            print 'Maybe you forget the index in %d' % self.NodeIndex+1
        else:
            self.NodeIndex = int(self.RPIndex.search(target).group(0))

        if self.RPBackground.search(target):
            self.Background = self.RPBackground.search(target).group(1)

        if self.RPBGM.search(target):
            self.BGM = self.RPBGM.search(target).group(1)

        if self.RPText.search(target):
            t = self.RPText.search(target).group(1)
            t = t.split(':')
            if len(t) == 1:
                self.Name = ''
                self.Text = t[0]
            elif len(t) == 2:
                self.Name,self.Text = t
            else:
                self.Name,SubList = (t[0],t[1:])
                self.Text = ':'.join(SubList)


        ## Value in self.Portrait will storage
        ## except occur {}
        ## which will make Portrait drop the value
        if self.RPPortrait.search(target):
            target = self.RPPortrait.search(target).group(1)
            if target:
                self.Portrait = self.__parserPortrait(target)
            else:
                self.Portrait = {}


        self.ChoiceBranch = self.RPChoice.findall(target)


    ## A complex data struct....
    ## but I think this will work well?
    def __parserPortrait(self,target):
        portraits = {}
        target = target.split('\n')
        for element in target:
            portrait = {}
            element = element.split(';')
            ## The way of using eval is dangerous
            ## pray?
            portrait['name'] = eval(element[0])
            ## add the flag which means
            ## the image will remove
            if element[1] == '':
                portrait['flag'] = True
            else:
                for i in element[1:]:
                    i = i.split('.')
                    assert len(i) == 2
                    if int(i[0]) == 1:
                        portrait['clip_pos'] = eval(i[1])
                    elif int(i[0]) == 2:
                        portrait['size'] = eval(i[1])
                    elif int(i[0]) == 3:
                        portrait['screen_pos'] = eval(i[1])
                    else:
                        print 'Wrong Gammer.Please check %d' % self.NodeIndex  
                        raise SystemExit
            portraits[portrait['name']] = portrait
        return portraits

    ##only for using the compiled re exp
    def searchIndex(self,target):
        try:
            index = int(self.RPIndex.search(target).group(0))
        except:
            print 'Cannot find the Index'
            raise SystemExit,message
        return index

    def getNodeIndex(self):
        return self.NodeIndex

    def getBackground(self):
        return self.Background
    
    def getBGM(self):
        return self.BGM

    def getText(self):
        return self.Text

    def getName(self):
        return self.Name

    def getChoice(self):
        return self.ChoiceBranch

    def getPortrait(self):
        return self.Portrait
