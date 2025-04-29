import eyed3.id3
import eyed3.mp3
import os,re,tinytag,eyed3
from os import path
from lyricsgenius import Genius

###############################################
## copies text from lyrics textfile to mp3 tags
###############################################
def lyrics_text_to_tags(ldir):
    not_found='not_found.txt'

    aud=['.mp3'] #VALID FILES EXTENSIONS

    # ldir=path.join('c:',path.sep,'users','lbdkn','Music','Alex-G - Race')
    os.chdir(ldir)

    not_found_string='' #LIST OF FILES NOT FOUND
    not_mp3_string='' #LIST OF FILES THAT ARE N0T MP3
    for clown in os.listdir():
        if aud.count(path.splitext(clown)[1])>0: #if its an mp3 (valid file extension)

            #########################################
            ## Gets the title/song_name from mp3 tags
            #########################################
            try:
                swan=tinytag.TinyTag.get(clown)
                print(f'{tinytag.TinyTag.get(clown)}')
                song_name=swan.title
            except Exception as e:
                print(f'{path.join(ldir,clown)}')
                print(e.args)
                print(e)
            #########################################
            #########################################

            ##########################################
            ## saves tags to temporary ID3 tag object
            #########################################
            try:
                to_tag=eyed3.load(clown)
                temp_tag=eyed3.id3.Tag()
                temp_tag.artist=swan.artist
                temp_tag.title=swan.title
                temp_tag.album=swan.album
                temp_tag.track_num=swan.track
            except Exception as e:
                print(f'{path.join(ldir,clown)}')
                print(e.args)
                print(e)
            #########################################
            #########################################
            
            found=False

            
            ####################################################
            ## Searches every textfile in the directory
            ## finds the file that matches the current song name
            ## and sets the lyrics tag 
            ####################################################
            for txt_lyrics_file in os.listdir():
                if path.splitext(txt_lyrics_file)[1]=='.txt':
                    zname=path.splitext(txt_lyrics_file)[0].split('_')[1]
                    if zname.lower()==song_name.lower():
                        found=True
                        reddd=open(txt_lyrics_file,mode='rt',encoding="utf_8").read()
                        reddd=re.compile(r'Embed').sub('',reddd)
                        try:
                            temp_tag.lyrics.set(reddd)
                            to_tag.tag.lyrics.set(reddd)
                            to_tag.tag.save()
                        except Exception as e:
                            print(f'{path.join(ldir,clown)}\n{e.args}\n{e}')
            ####################################################
            ####################################################
            
            ############################################
            ## if found prints the tag info to screen
            ## if not it adds it to the not found string
            ############################################
            if found:
                print(f'{to_tag.tag.artist}\n{to_tag.tag.album}\n{to_tag.tag.title}\n{to_tag.tag.track_num}\n')
                # print(f'found: {song_name}')
            else:
                not_found_string=not_found_string+f'\n{song_name}'
                # print(f'not found: {song_name}')
            ############################################
            ############################################


        ########################
        ## if its not an mp3
        ## add to not mp3 string
        ########################
        else:
            # awa=['.mp3','.m4a','.opus','.flac']
            if ['.mp3','.m4a','.opus','.flac'].count(path.splitext(clown)[1])>0:
                not_mp3_string+=f'{clown}\n'
        ########################
        ########################


        ################################
        ## Lists files that aren't mp3
        ## and saves them to not_mp3.txt
        ################################
        if not_mp3_string!='':
            if not path.exists(path.join(ldir,'not_mp3.txt')):
                tow=open(path.join(ldir,'not_mp3.txt'),mode='xt',encoding='utf_8')
                tow.write(f'{not_mp3_string}')
                tow.close()
            else:
                os.remove(path.join(ldir,'not_mp3.txt'))
                tow=open(path.join(ldir,'not_mp3.txt'),mode='xt',encoding='utf_8')
                tow.write(f'{not_mp3_string}')
                tow.close()
        ################################
        ################################

    ##################################
    ## Lists files not found
    ## and saves them to not_found.txt
    ##################################
    if not_found_string.strip().lstrip()!='':
        not_found='not_found.txt'
        if path.exists(not_found):
            os.remove(not_found)
            fs=open(not_found,mode='xt',encoding="utf_8")
            fs.write(not_found_string)
            fs.close()
        else:
            fs=open(not_found,mode='xt',encoding="utf_8")
            fs.write(not_found_string)
            fs.close()
    ##################################
    ##################################

#############################################
## gets lyrics from genius and saves to txt
## the mp3 has to have a title and artist tag
#############################################
def lyrics_from_genius_to_text(ldir):
    os.chdir(ldir)
    genius_token=Genius('_hiNTlH2XuZnhZGrwg_ybsza0jMl1Cj3_Y7PekGNT1oA2B_xFnft7JYwkFBVV2eC') ## geniustoken
    for boom in os.listdir():
        try:
            zb=tinytag.TinyTag.get(boom)
        except:
            print('NOT AN AUDIO FILE')
            continue

        ############################
        ## formats the text filename
        nono=['/','\\',':','?','*','"','<','>','|'] #nonvalid characters in filename
        title=zb.title
        artist=zb.artist
        for nope in nono:
            title=title.replace(nope,'#$inv#$')
            artist=artist.replace(nope,'#$inv#$')
        sname='lyrics_'+title+'_'+artist+'.txt'
        ############################
        ############################

        print(f'title:{title}\nartist:{artist}\ntxt:{sname}\n****************')
        lyr=genius_token.search_song(zb.title,zb.artist) # gets lyrics

        ###################
        ## sets lyrics text
        ###################
        if type(lyr)==type(None) :
            ztxt="(instrumental)"
        else:
            ztxt=re.compile(r'[0-9]{0,6} Contributors.*Lyrics').sub('',lyr.lyrics)
        ###################
        ###################

        ###################################
        ## check if lyrics text file exists
        ## if not create one
        ###################################
        if not path.exists(sname):
            nips=open(sname,mode='xt',encoding='utf_8')
        else:
            fs=open(sname,'rt')
            redd=fs.read()
            fs.close()
            if redd=='' or redd==None:
                os.remove(sname)
                nips=open(sname,mode='xt',encoding='utf_8')
            else:
                continue
        ###################################
        ###################################

        ############################
        ## write to lyrics text file
        ############################
        nips.write(ztxt)
        nips.close()
        ############################
        ############################

########################################################
## GETS RID OF NONVALID TEXT IN FILENAME
## AND THEN IF THE PARSED TEXT EQUALS THE -real- PARAMETER
## RETURNS TRUE, ELSE FALSE
########################################################
def find_garbage(txt,real):
    # txt='lyrics_happy_inv_ugly_Car Seat Headrest'
    txt=re.compile(r'_inv_').sub('#$sym#$',txt)
    txt=txt.split('_')[1]
    # real='happy/ugly'
    non=['/','\\','?','*','"','<','>','|',':']
    for yep in non:
        suk=txt.replace('#$sym#$',yep) # get rid of nonvalid text from filename
        if suk==real: # if the parsed text equals the real name of the song return True
            return True
    return False # after getting rid of the nonvalid text, it doesn't match , return False

##############################
# SETS LYRICS MANUALLY.
# lemp3->mp3file 
# lirik-> txt file with lyrics
##############################
def set_lyrics(lempy3,lirik):
    tiny_mp3=tinytag.TinyTag.get(lempy3)
    try:
        ##################################
        # RETURN IF ALREADY HAS LYRICS SET
        ##################################
        if tiny_mp3.extra.get('lyrics')!=None:
            print(f'[[[[[[[F A G   W A S   A L R E A D Y   H E R E]]]]]]]\n{tiny_mp3.extra.get('lyrics')}')
            return
    except Exception as e:
        print(f'{e.args}\n{e}')
    
    eyes=eyed3.load(lempy3)
    tuturu=open(lirik,'rt',encoding='utf_8')
    lick=tuturu.read()
    lick=re.compile(r'Embed').sub('',lick)
    eyes.tag.lyrics.set(lick)
    eyes.tag.save()
    tiny_mp3=tinytag.TinyTag.get(lempy3)
    print(f'here:{tiny_mp3.extra.get('lyrics')}')
    

#######################################################################################
## reads lyrics not found from not_found.txt
## then for every song filename in not_found.txt
## it gets rid of tabs and newlines and whitespace
## then it goes through all the files in the same directory
## and sends the mp3 files to find_garbage
## where it gets rid of non valid symbols from the filename
## after the mp3filename is parsed, if the text is the same as the one in not_found.txt 
## it sets the lyrics manually
#######################################################################################
def lost_found(andy):   
    ## andy -> path to look for not_found.txt 
    os.chdir(andy) # set to current directory
    mp3=[]
    ltxt=[]
    if os.listdir().count('not_found.txt')>0: # if not_found.txt exists
        fs=open('not_found.txt','rt',encoding='utf_8') # open as read text
        mp3=fs.readlines() ## save every song not found in not_found.txt into mp3[]
        fs.close() # close stream
        for song_not_found in mp3:
            chk=re.compile('\n').sub('',song_not_found) # get rid of newlines
            chk=re.compile('\t').sub('',song_not_found) # get rid of tabs
            chk=chk.strip() # get rid of whitespace at the left
            chk=chk.rstrip() # get rid of whhitespace at right
            if chk=='':continue # if its empty skip on to the next not found song


            song_not_found=song_not_found.replace('\n','')
            for mp3_file0 in os.listdir(): # check every file in current directory -andy-
                if path.splitext(mp3_file0)[1]=='.mp3': # if its an mp3 file
                    tiny_mp3=tinytag.TinyTag.get(mp3_file0) # get tags from mp3file
                    if tiny_mp3.title==song_not_found: # if the title on the tags is the same as the song in not_found.txt
                        for lyrics_text_file in os.listdir(): # check every file in current directory -andy-
                            if path.splitext(lyrics_text_file)[1]=='.txt': # if its a txt file 
                                if find_garbage(path.splitext(lyrics_text_file)[0],song_not_found): ## if after getting rid of symbols the names match, we've found it
                                    print(f'FOUND IT:{lyrics_text_file}\n{mp3_file0}')
                                    set_lyrics(lempy3=mp3_file0, lirik=lyrics_text_file) ## set lyrics manually(mp3 file, text file)


# os.chdir(path.join('c:',path.sep,'users','lbdkn','Music','Cavetown - Dear'))
# # set_lyrics('The Beatles - The Beatles - Why Don\'t We Do It In The Road？.mp3','lyrics_Why Don\'t We Do It in the Road#$inv#$_The Beatles.txt')
# lyrics_from_genius_to_text(path.join('c:',path.sep,'users','lbdkn','Music','Cavetown - Dear'))
# lyrics_text_to_tags(path.join('c:',path.sep,'users','lbdkn','Music','Cavetown - Dear'))


if __name__ == "__main__":
    input0 = input('Use current directory? y/n ')
    if input0.lower() == 'y':
        lyrics_from_genius_to_text(os.getcwd())
        lyrics_text_to_tags(os.getcwd())
    else:
        print('run from mp3 directory..')