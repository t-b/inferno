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
        self.PICKLEPATH=PICKLEPATH
        self.CSVPATH=CSVPATH
        self.csvFile= self.openFile(CSVPATH,'t') #FIXME probably should actually test this for bad inputs...
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
                    mode = 'r'+fileType #we open in read mode to keep a lock
                else:
                    raise TypeError('What kind of file is this?!')
                try:
                    return open( PATH , mode )
                except PermissionError:
                    self.cleanup()
                    raise PermissionError('The file is open somewhere! Close that program first.')

        else:
            return open( PATH , 'x'+fileType )

    def loadPickle(self, PATH): #ick had to use this to prevent EOFErrors
        try:
            f = open( PATH , 'rb' )
            self.saved_data=pickle.load( f )
        except EOFError:
            if os.path.getsize(PATH) == 0:
                self.saved_data={}
            else:
                raise IOError('Your pickle file has data but we get an EOFError... anyway. Size = %s'%os.path.getsize(PATH) )
        finally:
            f.close()

    def updatePickle(self,data):
        try:
            self.saved_data.update(data)
        except ValueError: #MUST have this here or we loose ALL the data in the file! (WTF)
            print('The data you just passed in is not a dictionary!')
            raise #prevent opening in write mode

        self.pickleFile.close()
        writePickle = open( self.PICKLEPATH, 'wb' )
        pickle.dump( self.saved_data , writePickle )
        writePickle.close()
        self.pickleFile = self.openFile( self.PICKLEPATH, 'b' )

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
        #d.updatePickle({1:'WILL IT WORK!?!'})
        #d.updatePickle('asdfasdfasdfasdfasdf')

        d.loadPickle('pickletest.pickle')

    #csvTest()
    pickleTest()

    d.cleanup()

if __name__ == '__main__':
    main()
