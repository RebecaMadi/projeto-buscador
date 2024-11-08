
class Lawsuit:
    """ Classe para a formatação de processos """
    
    def __init__(self, obj):
        self.lawsuit = {}
        self.set_id(obj)
        self.set_number(obj)
        self.set_date(obj)
        self.set_activities(obj)
        self.set_related_people(obj)
        self.set_lawyers(obj)
        self.set_value(obj)
        self.set_court(obj)
        self.lawsuit["instance"] = '1'
        self.set_kind(obj)
        self.set_nature(obj)
        self.set_subject(obj)
        self.set_judge(obj)

    def set_id(self, obj):
        self.lawsuit["id"] = obj["_id"]

    def set_number(self, obj):
        self.lawsuit["number"] = obj["_source"]["number"]
    
    def set_date(self, obj):
        if obj["_source"].get("date"):
            self.lawsuit["distributionDate"] = obj["_source"]["date"]

    def set_court(self, obj):
        if obj["_source"].get("court"):
                self.lawsuit["court"] = obj["_source"]["court"]

    def set_value(self, obj):
        if obj["_source"].get("value"):
            self.lawsuit["caseValue"] = obj["_source"]["value"]

    def set_nature(self, obj):
        if obj.get("highlight", {}).get("nature"):
            self.lawsuit["nature"] = obj["highlight"]["nature"][0]
        elif obj["_source"].get("nature"):
            self.lawsuit["nature"] = obj["_source"]["nature"]

    def set_kind(self, obj):
        if obj.get("highlight", {}).get("kind"):
            self.lawsuit["type"] = obj["highlight"]["kind"][0]
        elif obj["_source"].get("kind"):
            self.lawsuit["type"] = obj["_source"]["kind"]

    def set_subject(self, obj):
        if obj.get("highlight", {}).get("subject"):
            self.lawsuit["subject"] = obj["highlight"]["subject"][0]
        elif obj["_source"].get("subject"):
            self.lawsuit["subject"] = obj["_source"]["subject"]

    def set_judge(self, obj):
        if obj.get("highlight", {}).get("judge"):
            self.lawsuit["judge"] = obj["highlight"]["judge"][0]
        elif obj["_source"].get("judge"):
            self.lawsuit["judge"] = obj["_source"]["judge"]

    def set_related_people(self, obj):
        if obj["_source"].get("related_people"):
            self.lawsuit["related_people"] = []
            for i, person in enumerate(obj["_source"].get("related_people", [])):
                aux = {}
                if not obj.get("highlight", {}).get(f"related_people.name[{i}]") :
                    aux["name"] = person["name"]
                else:
                    aux["name"] = obj.get("highlight")[f"related_people.name[{i}]"][0]
                
                if not obj.get("highlight", {}).get(f"related_people.role[{i}]") :
                    aux["role"] = person["role"]
                else:
                    aux["role"] = obj.get("highlight")[f"related_people.role[{i}]"][0]

                self.lawsuit["related_people"].append(aux)

    def set_lawyers(self, obj):
        if obj["_source"].get("lawyers"):
            self.lawsuit["representedPersonLawyers"] = []
            for i, lawyer in enumerate(obj["_source"].get("lawyers", [])):
                aux = {}
                if not obj.get("highlight", {}).get(f"lawyers.name[{i}]"):
                    aux["name"] = lawyer["name"] 
                    aux["representedPerson"] = "NULL"
                else:
                    aux["name"] = obj.get("highlight")[f"lawyers.name[{i}]"][0]
                    aux["representedPerson"] = "NULL"
                    
                self.lawsuit["representedPersonLawyers"].append(aux)

    def set_activities(self, obj):
        if obj["_source"].get("activities"):
            self.lawsuit["movements"] = obj["_source"]["activities"]