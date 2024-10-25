
class Lawsuit:
    """ Classe para a formatação de processos """
    
    def __init__(self, obj):
        self.lawsuit = {}
        self.get_id(obj)
        self.get_number(obj)
        self.get_court(obj)
        self.get_nature(obj)
        self.get_kind(obj)
        self.get_subject(obj)
        self.get_date(obj)
        self.get_judge(obj)
        self.get_value(obj)
        self.get_related_people(obj)
        self.get_lawyers(obj)
        self.get_activities(obj)

    def get_id(self, obj):
        self.lawsuit["id"] = obj["_id"]

    def get_number(self, obj):
        self.lawsuit["number"] = obj["_source"]["number"]
    
    def get_date(self, obj):
        if obj["_source"].get("date"):
            self.lawsuit["date"] = obj["_source"]["date"]

    def get_court(self, obj):
        if obj["_source"].get("court"):
                self.lawsuit["court"] = obj["_source"]["court"]

    def get_value(self, obj):
        if obj["_source"].get("value"):
            self.lawsuit["value"] = obj["_source"]["value"]

    def get_nature(self, obj):
        if obj.get("highlight", {}).get("nature"):
            self.lawsuit["nature"] = obj["highlight"]["nature"][0]
        elif obj["_source"].get("nature"):
            self.lawsuit["nature"] = obj["_source"]["nature"]

    def get_kind(self, obj):
        if obj.get("highlight", {}).get("kind"):
            self.lawsuit["kind"] = obj["highlight"]["kind"][0]
        elif obj["_source"].get("kind"):
            self.lawsuit["kind"] = obj["_source"]["kind"]

    def get_subject(self, obj):
        if obj.get("highlight", {}).get("subject"):
            self.lawsuit["subject"] = obj["highlight"]["subject"][0]
        elif obj["_source"].get("subject"):
            self.lawsuit["subject"] = obj["_source"]["subject"]

    def get_judge(self, obj):
        if obj.get("highlight", {}).get("judge"):
            self.lawsuit["judge"] = obj["highlight"]["judge"][0]
        elif obj["_source"].get("judge"):
            self.lawsuit["judge"] = obj["_source"]["judge"]

    def get_related_people(self, obj):
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

    def get_lawyers(self, obj):
        if obj["_source"].get("lawyers"):
            self.lawsuit["lawyers"] = []
            for i, lawyer in enumerate(obj["_source"].get("lawyers", [])):
                aux = {}
                if not obj.get("highlight", {}).get(f"lawyers.name[{i}]"):
                    aux["name"] = lawyer["name"] 
                else:
                    aux["name"] = obj.get("highlight")[f"lawyers.name[{i}]"][0]
                    
                self.lawsuit["lawyers"].append(aux)

    def get_activities(self, obj):
        if obj["_source"].get("activities"):
            self.lawsuit["activities"] = obj["_source"]["activities"]