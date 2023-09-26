# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet,  FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random

PHQ4 = [
    'في حدود الأسبوعين الي فاتم قد ايه كنت بتحس إنك متضايق أو متوتر أو علي أخرك ؟',  # Anxiety
    'طيب قد ايه برضه كنت مخنوق بسبب إنك مش عارف توقف أو تتحكم في قلقك ؟',  # Anxiety
    'طيب هل كنت بتحس بإنك فاقد المتعة أو الإهتمام وأنت بعمل اي حاجة ؟',  # Depression
    'طيب كنت قد ايه مخنوق بسبب الشعور بالإحباط أو اليأس أو الإكتئاب ؟',  # Depression
]

PHQ_REST = [
    'هل عندك مشاكل في النوم ؟ ',
    'هل بتحس بالتعب أو إنك عندك طاقة قليلة ؟',
    'عندك قلة شهية أو بتاكل كتير أكتر من المعتاد ؟',
    'حاسس بإنك مش راضي عن نفسك أو إنك خزلت كل الناس الي حواليك ؟',
    'عندك صعوبة في التركيز وأنت بتقرأ أو إنك بتشاهد التلفزيون ؟',
    'عندك بطئ في الحركة أو الكلام بشكل ملحوظ أو بتتكلم بسرعة أو بتتحرك بسرعة ؟',
    'راودتك أفكار بأنه من الأفضل لو كنت ميتا أو أفكار بأن تقوم بإيذاء نفسك ؟'
]

GAD_REST = [
    'الشعور بالقلق والهم الزائد حول الأمور ؟',
    'الإحساس بصعوبة في الإسترخاء ؟',
    'الشعور بعدم الإستقرار لدرجة تصعب عليك فيها الجلوس بلا حركة ؟',
    'الإنفعال أو الإنزعاج بسهولة ؟',
    'الشعور بالخوف وكأن شيئ مريع قد يحدث لك ؟'
]

buttons = [
    {'title': 'نهائي 😇', 'payload': 'نهائي 😇'},
    {'title': 'أيام قليلة 🙂', 'payload': 'أيام قليلة 🙂'},
    {'title': 'أغلب الأيام 😕', 'payload': 'أغلب الأيام 😕'},
    {'title': 'كل الأيام 😫', 'payload': 'كل الأيام 😫'},
]

answers = [
    'نهائي 😇',
    'أيام قليلة 🙂',
    'أغلب الأيام 😕',
    'كل الأيام 😫',
]

GAD_tips = [
    "إعمل تمرين 5×3 ببساطة عايزك تمارس رياضة زي الجري ركوب العجل أو المشي 3 أو 5 مرات في الأسبوع لمدة 30 دقيقة وأهم "
    "حاجة المواظبة 🤗🤗",
    "حاول تحط روتين يومي بسيط بإنك تحط أهداف يومك لمدة 15 أو 30 دقيقة بالكتير ❤️❤️",
    " 🤝 حاول تلاقي أشخاص تساعدوا بعض علي الرياضة زي الإنضمام لنادي أو غيره ده من شأنه يقلل حدة الإكتئاب"
]

PHQ_tips = [
    "لا تنسحب من الحياة. يمكن أن يحسن التواصل الاجتماعي مزاجك. يعني البقاء على اتصال مع الأصدقاء والعائلة أن لديك "
    "شخصًا تتحدث إليه عندما تشعر بالإكتئاب",
    "كن أكثر نشاطا. مارس نوعًا من التمارين. هناك أدلة على أن التمرين يمكن أن يساعد في تحسين مزاجك. إذا لم تكن قد "
    "مارست الرياضة لفترة ، فابدأ بلطف بالمشي لمدة 20 دقيقة كل يوم.",
    "لا تتجنب الأشياء التي تجدها صعبة. عندما يشعر الناس بالإحباط أو القلق ، فإنهم يتجنبون أحيانًا التحدث إلى الآخرين. "
    "قد يفقد بعض الناس ثقتهم في الخروج أو القيادة أو السفر. إذا بدأ هذا في الحدوث ، فإن مواجهة هذه المواقف ستساعدها "
    "على أن تصبح أسهل.",
    "حاول أن تأكل نظامًا غذائيًا صحيًا. لا يشعر بعض الأشخاص بالرغبة في تناول الطعام عند الإصابة بالاكتئاب ويكونون "
    "عرضة لخطر الإصابة بنحافة الوزن. يجد البعض الآخر الراحة في الطعام ويمكن أن يزيد الوزن. "
]

depression_links = [
    'https://adaa.org/understanding-anxiety/depression/tips'
    'https://adaa.org/understanding-anxiety/depression/treatment-management'
]

out_scope = "حاول تتصاول مع أخصائي نفسه من شأنه إنه يعرف يساعدك بطريقة أحسن 🤗 🤗"

suicidal = "عندي شوية صحاب من الأزهر ممكن يساعدوك أحسن مني بكتير جرب تتصل عليهم 0020225973500 🤗 🤗 وخليك فاكر إن " \
           "الإنتحار مش الحل والموضوع أسهل بكتير 💜💙💜💙 "


class PHQ4Test(Action):

    def name(self) -> Text:
        return "PHQ4Test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        qindex = tracker.get_slot('Qindex')
        msg = PHQ4[qindex]
        dispatcher.utter_message(text=msg, buttons=buttons)
        return [SlotSet('Qindex', qindex + 1)]


class PHQ4Scorer(Action):

    def name(self) -> Text:
        return "PHQ4Scorer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        qindex = tracker.get_slot('Qindex') - 1
        last_answer = tracker.latest_message['text']
        setting = []
        if qindex < 2:  # This is for anx
            score = tracker.get_slot('PHQ4_anx')
            test_answers = tracker.get_slot('GAD7_answers')
            if last_answer == answers[1]:
                setting.append(SlotSet('PHQ4_anx', score + 1))
                test_answers.append(1)
            elif last_answer == answers[2]:
                setting.append(SlotSet('PHQ4_anx', score + 2))
                test_answers.append(2)
            elif last_answer == answers[3]:
                setting.append(SlotSet('PHQ4_anx', score + 3))
                test_answers.append(3)
            else:
                test_answers.append(0)
            setting.append(SlotSet('GAD7_answers', test_answers))

        else:
            score = tracker.get_slot('PHQ4_dep')
            test_answers = tracker.get_slot('PHQ9_answers')
            if last_answer == answers[1]:
                setting.append(SlotSet('PHQ4_dep', score + 1))
                test_answers.append(1)
            elif last_answer == answers[2]:
                setting.append(SlotSet('PHQ4_dep', score + 2))
                test_answers.append(2)
            elif last_answer == answers[3]:
                setting.append(SlotSet('PHQ4_dep', score + 3))
                test_answers.append(3)
            else:
                test_answers.append(0)
            setting.append(SlotSet('PHQ9_answers', test_answers))
        return setting


class AfterP4(Action):
    def name(self) -> Text:
        return 'AfterP4'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        setting = []
        dep_score = tracker.get_slot('PHQ4_dep')
        anx_score = tracker.get_slot('PHQ4_anx')
        setting.append(SlotSet('PHQ9', dep_score))
        setting.append(SlotSet('GAD7', anx_score))
        setting.append(SlotSet('Qindex', 0))
        phq9, gad7 = False, False
        if dep_score >= 3:
            phq9 = True
        if anx_score >= 3:
            gad7 = True
        if phq9 and ~gad7:
            setting.append(SlotSet('PHQ9_applicable', True))
        if ~phq9 and gad7:
            setting.append(SlotSet('GAD7_applicable', True))
        if phq9 and gad7:
            setting.append(SlotSet('Both_applicable', True))
        return setting


class PHQ9Test(Action):
    def name(self) -> Text:
        return 'PHQ9Test'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        qindex = tracker.get_slot('Qindex')
        print("PHQ9Test gen working!" , qindex)
        # print("PHQ9Scorer working!")
        setting = []
        # last_answer = tracker.latest_message['text']
        # score = tracker.get_slot('PHQ9')
        # test_answers = tracker.get_slot('PHQ9_answers')
        # if last_answer == answers[1]:
        #     setting.append(SlotSet('PHQ9', score + 1))
        #     test_answers.append(1)
        # elif last_answer == answers[2]:
        #     setting.append(SlotSet('PHQ9', score + 2))
        #     test_answers.append(2)
        # elif last_answer == answers[3]:
        #     setting.append(SlotSet('PHQ9', score + 3))
        #     test_answers.append(3)
        # else:
        #     test_answers.append(0)
        # setting.append(SlotSet('PHQ9_answers', test_answers))
        
        # If all questions have been asked, end the questionnaire
        if qindex >= len(PHQ_REST):
            dispatcher.utter_message("شكرا لإتمامك الاختبار")
            print("Tips working!")
            phq_answers = tracker.get_slot('PHQ9_answers')
            phq_score = tracker.get_slot('PHQ9')
            print(phq_score)
            if phq_score <= 4:
                result = "عدم وجود مشكلة"
            elif phq_score <= 9:
                result = "اكتئاب بسيط"
            elif phq_score <= 14:
                result = "اكتئاب متوسط"
            elif phq_score <= 19:
                result = "اكتئاب شديد"
            else:
                result = "اكتئاب حاد"
                
            if len(phq_answers) == 7:
                if phq_answers[-1] >= 2:  # Suicidal thoughts support
                    dispatcher.utter_message('نتيجة الاختبار تشير إلى أن لديك ميول انتحارية')
                    dispatcher.utter_message(suicidal)
                # elif phq_score >= 10:  # We only help till mild
                #     dispatcher.utter_message(out_scope)
                # else:
                #     dispatcher.utter_message(random.choice(PHQ_tips))
                dispatcher.utter_message(text=f"نتيجة الاختبار تشير إلى {result}")
        # elif len(gad_answers) == 7:
        #     # if gad_score >= 10:  # We only help till mild
        #     #     dispatcher.utter_message(out_scope)
        #     # else:
        #     # dispatcher.utter_message(random.choice(GAD_tips))
        #     dispatcher.utter_message(text=f"نتيجة الاختبار تشير إلى {result_anxiety}")
        # return []
            setting.append(SlotSet('Qindex', 0))
            return setting
        # if qindex + 1 != len(PHQ_REST):
        msg = PHQ_REST[qindex]
        setting.append(SlotSet('Qindex', qindex + 1))
        dispatcher.utter_message(text=msg, buttons=buttons)
        # else:
        #     return []

        # if qindex + 1 == len(PHQ_REST):
            # dispatcher.utter_message(text="تم الاختبار")
            # return [SlotSet('Qindex', 0), SlotSet('PHQ9_applicable', False)]

        return setting


class GAD7Test(Action):
    def name(self) -> Text:
        return 'GAD7Test'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        qindex = tracker.get_slot('Qindex')
        msg = GAD_REST[qindex]
        dispatcher.utter_message(text=msg, buttons=buttons)

        return [SlotSet('Qindex', qindex + 1)]


class PHQ9Scorer(Action):
    def name(self) -> Text:
        return 'PHQ9Scorer'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        setting = []
        last_answer = tracker.latest_message['text']
        score = tracker.get_slot('PHQ9')
        test_answers = tracker.get_slot('PHQ9_answers')
        if last_answer == answers[1]:
            setting.append(SlotSet('PHQ9', score + 1))
            test_answers.append(1)
        elif last_answer == answers[2]:
            setting.append(SlotSet('PHQ9', score + 2))
            test_answers.append(2)
        elif last_answer == answers[3]:
            setting.append(SlotSet('PHQ9', score + 3))
            test_answers.append(3)
        else:
            test_answers.append(0)
        setting.append(SlotSet('PHQ9_answers', test_answers))
        return setting


class GAD7Scorer(Action):
    def name(self) -> Text:
        return 'GAD7Scorer'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        setting = []
        last_answer = tracker.latest_message['text']
        score = tracker.get_slot('GAD7')
        test_answers = tracker.get_slot('GAD7_answers')
        if last_answer == answers[1]:
            setting.append(SlotSet('GAD7', score + 1))
            test_answers.append(1)
        elif last_answer == answers[2]:
            setting.append(SlotSet('GAD7', score + 2))
            test_answers.append(2)
        elif last_answer == answers[3]:
            setting.append(SlotSet('GAD7', score + 3))
            test_answers.append(3)
        else:
            test_answers.append(0)
        setting.append(SlotSet('GAD7_answers', test_answers))
        return setting


class Show(Action):  # This class is for debugging
    def name(self) -> Text:
        return 'show'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('name')
        index = tracker.get_slot('Qindex')
        PHQ4_dep = tracker.get_slot('PHQ4_dep')
        PHQ4_anx = tracker.get_slot('PHQ4_anx')
        PHQ9 = tracker.get_slot('PHQ9')
        GAD7 = tracker.get_slot('GAD7')
        PHQ9_answers = tracker.get_slot('PHQ9_answers')
        GAD7_answers = tracker.get_slot('GAD7_answers')
        phq9_app = tracker.get_slot('PHQ9_applicable')
        gad7_app = tracker.get_slot("GAD7_applicable")
        both_app = tracker.get_slot("Both_applicable")
        results = f"name: {name} \n Qindex {index} \n PHQ4_dep {PHQ4_dep} " \
                  f"\n PHQ4_anx {PHQ4_anx} \n PHQ9 {PHQ9} \n GAD7 {GAD7} \n" \
                  f"'PHQ9 answers {PHQ9_answers} \n" \
                  f"GAD7 answers  {GAD7_answers} \n" \
                  f"PHQ9_Applicable {phq9_app} \n" \
                  f"GAD7_applicable {gad7_app} \n" \
                  f"Both_applicable {both_app}"
        dispatcher.utter_message(text=results)
        return []


class Tips(Action):
    def name(self) -> Text:
        return 'tip'

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        print("Tips working!")
        gad_answers = tracker.get_slot('GAD7_answers')
        phq_answers = tracker.get_slot('PHQ9_answers')
        phq_score = tracker.get_slot('PHQ9')
        print(phq_score)
        gad_score = tracker.get_slot('GAD7')
        if phq_score <= 4:
            result = "عدم وجود مشكلة"
        elif phq_score <= 9:
            result = "اكتئاب بسيط"
        elif phq_score <= 14:
            result = "اكتئاب متوسط"
        elif phq_score <= 19:
            result = "اكتئاب شديد"
        else:
            result = "اكتئاب حاد"
            
        if gad_score <= 4:
            result_anxiety = "عدم وجود مشكلة"
        elif gad_score <= 9:
            result_anxiety = "قلق بسيط"
        elif gad_score <= 14:
            result_anxiety = "قلق متوسط"
        elif gad_score <= 19:
            result_anxiety = "قلق شديد"
        else:
            result_anxiety = "قلق حاد"

        if len(phq_answers) == 7:
            if phq_answers[-1] >= 2:  # Suicidal thoughts support
                dispatcher.utter_message('نتيجة الاختبار تشير إلى أن لديك ميول انتحارية')
                dispatcher.utter_message(suicidal)
            # elif phq_score >= 10:  # We only help till mild
            #     dispatcher.utter_message(out_scope)
            # else:
            #     dispatcher.utter_message(random.choice(PHQ_tips))
            dispatcher.utter_message(text=f"نتيجة الاختبار تشير إلى {result}")
        elif len(gad_answers) == 7:
            # if gad_score >= 10:  # We only help till mild
            #     dispatcher.utter_message(out_scope)
            # else:
            # dispatcher.utter_message(random.choice(GAD_tips))
            dispatcher.utter_message(text=f"نتيجة الاختبار تشير إلى {result_anxiety}")
        return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Dict, List, Text
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class CallClassifierAPIAction(Action):
    def name(self) -> Text:
        return "action_call_classifier_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the last two user messages from the tracker
        
        last_two_messages = tracker.events[-3:]
        texts = []
        setting = []
        for message in last_two_messages:
            if 'text' in message and message.get("event") == "user":
                texts.append(message.get("text"))

        # print("Texts:", texts[0])

        # # Make a request to the local API
        response = requests.post('http://localhost:8080/predict', json={'text': str(texts[0])})

        # Process the API response
        if response.status_code == 200:
            output = response.json()
            sentiment_1 = output.get('sentiment_1')
            sentiment_2 = output.get('sentiment_2')
            # print('\n', sentiment_1, '\n', sentiment_2)
            setting.append(SlotSet('sentiment_1', sentiment_1))
            # setting.append(SlotSet('sentiment_2', sentiment_2))
        #     # Send the output back to the user
            # dispatcher.utter_message(text="تقديم الحالة النفسية للمريض (مؤقتا إلى أن يتم دمج الداتا بيز وتقديم نصاحئ للمريض)")
            # dispatcher.utter_message(text=f"يبدو أن المريض يعاني من: {sentiment_1} أو: {sentiment_2}")
            # dispatcher.utter_message(text="")
        #     dispatcher.utter_message(text=f"PHQ9_applicable: {tracker.get_slot('PHQ9_applicable')}")
        #     dispatcher.utter_message(text=f"{tracker.get_slot('sentiment_1')}")
        #     # Set PHQ9_applicable slot if sentiment_1 is "depression"
            # if sentiment_1 == "depression" or sentiment_2 == "depression":
            #     print('\n', "depression")
            #     setting.append(SlotSet('PHQ9_applicable', True))
            #     return setting
        # else:
        #     dispatcher.utter_message(text="Failed to call the local API.")
        return setting

from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ConversationPaused, UserUtteranceReverted
   
class ActionDefaultFallback(Action):
    def name(self) -> Text:
            return "action_default_fallback"
    def run(self, dispatcher, tracker, domain):
            # output a message saying that the conversation will now be
            # continued by a human.
    
            message = "آسف مش قادر أفهمك ، ممكن توضحلي أكتر"
            dispatcher.utter_message(text=message)
    # pause tracker
            # undo last user interaction
            return [ConversationPaused(), UserUtteranceReverted()]