import os
import pickle

class dataio: #TODO if we are REALLY paranoid we can open the file back up and check that it matches what we have in memory...
    """ class to manage input and output of data to disk
    this way we can retain a lock on the files for the
    duration of our program run time and not have nasty
    'oh you opened that file half way through running'
    errors
    """
    def __init__(self,PICKLEPATH,CSVPATH):
        self.PICKLEPATH=PICKLEPATH
        self.CSVPATH=CSVPATH
        self.csvFile = self.openFile(CSVPATH,'t') #FIXME probably should actually test this for bad inputs...
        self.pickleFile = self.openFile(PICKLEPATH,'b')

    def __enter__(self):
        return self 

    def openFile(self,PATH,fileType):
        """ ALWAYS open READ """
        if os.path.exists(PATH):
            if not os.path.isfile(PATH):
                 raise IOError( 'Path is not a file!' )
            else:
                if fileType == 'b':
                    self.saved_data = self.loadPickle()
        else:
            f = open( PATH , 'x'+fileType ) #create the file since it doesnt exist
            f.close()
            if fileType == 'b':
                self.saved_data = {} #if the file doesnt exist there is no saved data!

        mode = 'r'+fileType
        try:
            return open( PATH , mode )
        except PermissionError:
            self.cleanup()
            raise PermissionError('The file is open somewhere! Close that program first.')

    def loadPickle(self):
        try:
            self.pickleFile.close()
        except AttributeError:
            pass #its ok this happens at first run
        try:
            f = open( self.PICKLEPATH , 'rb' )
            return pickle.load( f )
        except EOFError:
            if os.path.getsize(self.PICKLEPATH) == 0:
                return {}
            else:
                raise IOError('Your pickle file has data but we get an EOFError... anyway. Size = %s'%os.path.getsize(PATH) )
        finally:
            f.close()
            self.pickleFile = open( self.PICKLEPATH , 'rb' )

    def updatePickle(self,data):
        try:
            self.saved_data.update(data)
        except ValueError: #MUST have this here or we loose ALL the data in the file! (WTF)
            print('The data you just passed in is not a dictionary!')
            raise #prevent opening in write mode

        self.pickleFile.close()
        with open( self.PICKLEPATH, 'wb' ) as writePickle:
            pickle.dump( self.saved_data , writePickle )
        self.pickleFile = open( self.PICKLEPATH, 'rb' )

    def loadCSV(self):
        self.csvFile.close() 
        with open ( self.CSVPATH , 'rt' ) as f:
            output = f.read()
        self.csvFile = open ( self.CSVPATH , 'rt' )
        return output 

    def updateCSV(self,textData):
        """ PREPEND YOUR STRINGS WITH NEWLINES OR SUFFER THE CONSEQUENCES """
        lines=self.loadCSV()
        if lines.count('HS'):
            if textData[0] != '\n':
                raise TypeError('textData MUST start with a newline!')
            else:
                textData = '\n'+textData.split('\n',2)[2]
        else:
            textData.strip('\n') #a new csv file so dont put a newline first

        self.csvFile.close()
        with open( self.CSVPATH , 'at' ) as csvWrite:
            csvWrite.writelines(textData)
        self.csvFile = open( self.CSVPATH , 'rt' )

    def __exit__(self,type,value,traceback):
        self.csvFile.close()
        self.pickleFile.close()



def main():
    from IPython import embed
    from output import makeText #bloodly pywin32 being pulled in by this
    from config import ROW_ORDER,ROW_NAMES,OFF_STRING

    #d=dataio('pickletest.pickle','csvtest.csv')

    sample_data = { 'asdf filename.abf':(1,{1:'really?'}),
                    'asdf filename2.abf':(1,{2:'really?'}),
                    'asdf filename3.abf':(1,{3:'really?'}),
                  }
    update_data = {
        'did this update work?':(2,{'ALL THE THINGS':'NOPE'}),
        '2 did this update work?':(2,{'ALL THE THINGS':'NOPE'}),
    }

    with dataio('nrw.pickle','nrw.csv') as nrw , dataio('nwr.pickle','nwr.csv') as nwr:
        print(nrw.loadCSV())
        print(nrw.loadPickle())
        nrw.updatePickle(sample_data)
        nrw.updatePickle( makeText(sample_data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter=',') )
        nrw.updatePickle(update_data)
        nrw.updatePickle( makeText(update_data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter=',') )

        nwr.updatePickle(sample_data)
        nwr.updatePickle( makeText(sample_data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter=',') )
        print(nwr.loadCSV())
        print(nwr.loadPickle())
        nwr.updatePickle(update_data)
        nwr.updatePickle( makeText(update_data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter=',') )

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
    #pickleTest()

    #d.cleanup()

if __name__ == '__main__':
    main()
