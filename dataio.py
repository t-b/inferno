import os
import pickle

class dataio:
    """ class to manage input and output of data to disk
    this way we can retain a lock on the files for the
    duration of our program run time and not have nasty
    'oh you opened that file half way through running'
    errors
    """
    def __init__(self,PICKLEPATH,CSVPATH):
        #self.PICKLEPATH=PICKLEPATH
        #self.CSVPATH=CSVPATH
        self.csvFile= self.openFile(CSVPATH,'t')
        self.pickleFile= self.openFile(PICKLEPATH,'b')
    def cleanup(self):
        self.csvFile.close()
        self.pickleFile.close()

    def openFile(self,PATH,fileType):
        if os.path.exists(PATH):
            if not os.path.isfile(PATH):
                 raise IOError( 'Path is not a file!' )
            else:
                if fileType == 't':
                    mode = 'a+'+fileType
                elif fileType == 'b':
                    self.loadPickle(PATH)
                    mode = 'w'+fileType #we rewrite the pickle
                else:
                    raise TypeError('What kind of file is this?!')
                print(mode)
                try:
                    return open( PATH , mode )
                except PermissionError:
                    raise PermissionError('The file is open somewhere! Close that program first.')

        else:
            return open( PATH , 'x'+fileType )

    def loadPickle(self, PATH): #ick had to use this to prevent EOFErrors
        self.saved_data=pickle.load(open(PATH,'rb'))
        print(self.saved_data)
        #self.saved_data={}

    def updatePickle(self,data):
        self.saved_data.update(data)

        pickle.dump( self.saved_data , self.pickleFile ) #FIXME this is oneoff for writing right now

    def loadCSV(self):
        self.csvFile.seek(0)
        return self.csvFile.read()

    def updateCSV(self,textData):
        """ PREPEND YOUR STRINGS WITH NEWLINES OR SUFFER THE CONSEQUENCES """
        while 1: #loop to see if we already have HS line
            lines=self.loadCSV()
            if lines.count('HS'):
                if textData[0] != '\n':
                    raise TypeError('textData MUST start with a newline!')
                textData = '\n'+textData.split('\n',2)[2]
                #FIXME do we need to jump to the end?
                break
            elif line == '': #end if we don't find any
                break
        self.csvFile.writelines(textData)

def main():
    from IPython import embed
    d=dataio('pickletest.pickle','csvtest.csv')

    def csvTest():
        print(d.loadCSV())
        d.updateCSV('\nTHIS,LINE,SHOULD,NOT,BE,HERE\nTHIS,ONE,SHOULD,BE,HERE\netc\n\tetc')
        try:
            d.updateCSV('BADTHIS,LINE,SHOULD,NOT,BE,HERE\nTHIS,ONE,SHOULD,BE,HERE\netc\netc') #this should create an error
            failed=False
        except:
            failed=True
        assert failed, 'Bad string did not fail'
        print(d.loadCSV())

    def pickleTest():
        #embed()

        #d.updatePickle({2:'aaaaaaaaaaaaaaaaaaaa'})
        #d.updatePickle({4:'aaaaaabbbbbbbbbbb'})
        #d.updatePickle({'4sdf':'aaaaaabbbbbbbbbbb','zzz':'testing!'})
        d.updatePickle({1:'WILL IT WORK!?!'})

        #print(d.loadPickle())

    #csvTest()
    pickleTest()



    d.cleanup()

if __name__ == '__main__':
    main()