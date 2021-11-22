class StrategyBase:
    def __init__(self,id,name,description,initfunds,unit,sdate,edate,owner_id):
        self.id = id
        self.name = name
        self.description = description
        self.initfunds = initfunds
        self.unit = unit
        self.sdate = sdate
        self.edate = edate
        self.owner_id = owner_id