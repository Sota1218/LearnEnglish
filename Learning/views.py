from django.shortcuts import render,redirect
from Entrance.models import User,Dictionary
import random
from pykakasi import kakasi
from Learning.convertHelper import convert_to_romaji

# Create your views here.
def redirect_entrance(request):
    return redirect('/entrance')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/entrance')
    dictionary = Dictionary.objects.filter(creator = User.objects.get(id=request.session['user_id'])).order_by('-created_at')
    context = {
        "dictionary":dictionary
    }
    return render(request,"dashboard.html",context)

def addWord(request):
    if  request.POST['engWord'] and request.POST['japWord']:
        user_id = request.session['user_id']
        curr_user = User.objects.get(id = user_id)
        Dictionary.objects.create(englishWord=request.POST['engWord'],japaneseWord=request.POST['japWord'],creator=curr_user)
        return redirect('/learning')
    else:
        print("gagagaga")
        return redirect('/learning')

def delete(request,id):
    words_to_delete = Dictionary.objects.get(id=int(id))
    words_to_delete.delete()
    return redirect('/learning') 

def update(request,id):
    if  request.POST['editEng'] and request.POST['editJap']:
        edit_words = Dictionary.objects.get(id=int(id))
        edit_words.japaneseWord = request.POST['editJap']
        edit_words.englishWord = request.POST['editEng']
        print(edit_words)
        edit_words.save()
        return redirect('/learning')
    else:
        return redirect('/learning')

def logout(request):
    request.session.flush()
    return redirect("/")

######## Test Page ########

def test(request):
    if request.method == 'GET':
        dictionary = Dictionary.objects.filter(creator = User.objects.get(id=request.session['user_id']))
        context = {
            "dictionary":dictionary,
            "able_select":True
        }
        dictionary = Dictionary.objects.filter(creator = User.objects.get(id=request.session['user_id']))
        return render(request,"test.html",context)
    else:
        lang = request.POST['answerLanguage']
        num = int(request.POST['number'])
        rand = request.POST['random']
        dictionary = Dictionary.objects.filter(creator = User.objects.get(id=request.session['user_id']))
        wordsList = []

        if rand == '0':
            rand = True
        else:
            rand = False

        if len(dictionary) < num:
            return redirect('/test')
        request.session['numberOfQuestions'] = num
        japList = [i.japaneseWord for i in dictionary]
        engList = [i.englishWord for i in dictionary]
        if rand:
            iNum = [n for n in range(len(dictionary))]
            print(iNum)
            randomNum = random.sample(iNum,len(iNum))
            # a = sorted(iNum, key=lambda k: random.random())
            print(randomNum)
            # japList = [japList[randomNum[i]] for i in range(len(randomNum))]
            # engList = [engList[randomNum[i]] for i in range(len(randomNum))]
            request.session['japList'] = [japList[i] for i in randomNum]
            request.session['engList'] = [engList[i] for i in randomNum]
            print(japList)
        
        if lang == "jap":
            request.session['lang'] = "jap"
            return render(request,'test.html',context={'words':request.session['engList'][:num]})
        elif lang == "eng":
            request.session['lang'] = "eng"
            return render(request,'test.html',context={'words':request.session['japList'][:num]})
        else:
            #ランダムに問題を出す関数
            pass

def calculate(request):
    answers = request.POST.getlist('answers')
    score = 0
    wrongAnswers = []
    for i in range(len(answers)):
        if request.session['lang'] == "jap":
            romajiAns=convert_to_romaji(answers[i])
            romajiCorrectAns=convert_to_romaji(request.session['japList'][i])
            print(romajiAns)
            print(romajiCorrectAns)
            if romajiAns == romajiCorrectAns:
                score += 1
            else:
                wrongAnswers.append({
                    "user_answer":answers[i],
                    "correct_answer":request.session['japList'][i],
                    "question":request.session['engList'][i],
                    })
        elif request.session['lang'] == "eng":
            if answers[i] == request.session['engList'][i]:
                score += 1
                print(score)
            else:
                wrongAnswers.append({
                    "user_answer":answers[i],
                    "correct_answer":request.session['engList'][i],
                    "question":request.session['japList'][i],
                    })
    request.session['dictOfResult'] = {"score":score,"WA":wrongAnswers,"numOfQ":request.session['numberOfQuestions']}
    return redirect("/test/result")

def result(request):
    return render(request,"testResult.html")




