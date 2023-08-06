from flask import Flask,request, send_from_directory # Import Flask
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

import time
app = Flask(__name__) # Init Flask + API
api = Api(app)

# Swagger Code
@app.route('/swag/<path:path>')
def send_js(path):
    return send_from_directory('swag', path)
swaggerui_blueprints=get_swaggerui_blueprint('/swagger','/swag/swag.json',config={'app-name':'TimeKeeper'})
app.register_blueprint(swaggerui_blueprints,url_prefix='/swagger')


TimeKeeper=[] # Log Dictionary
def timeelapsed(sec): # Formatted Time Elapsed
    return time.strftime("%H:%M:%S", time.gmtime(sec))
def displog(reports): # Returns Formatted Time Log
    logged = reports.copy()
    if 'Stop' in logged: # Calculates Time and Prettify
        logged['Duration'] = timeelapsed(logged['Stop'] - logged['Start'])
        logged['Stop'] = time.ctime(logged['Stop'])
    else:
        logged['Elapsed'] = timeelapsed(time.time() - logged['Start'])
    logged['Start'] = time.ctime(logged['Start']) #NOTE: THIS IS INTENTIONALLY OUTSIDE THE ELSE BLOCK
    return logged
class CreateTracker(Resource):
    def __init__(self):
        pass
    def get(self,name): # Gets the Last Log of Provided Name
        for reports in reversed(TimeKeeper):
            if reports['Log'] == name:
                return displog(reports)
        if len(TimeKeeper) != 0:
            return {"Log":TimeKeeper[-1]}
        else:
            return {"Log":"Dead"}
    def post(self,name): # Creates a New Log and Ends Previous Log if it's continuing.
        if len(TimeKeeper) != 0:
            if not ('Stop' in TimeKeeper[-1]):
                TimeKeeper[-1]['Stop']=time.time()
        Tem= {'Log':name,'Summary':'http://127.0.0.1:5000/Summary/'+name,'Start':time.time()}
        TimeKeeper.append(Tem.copy())
        Tem['Start']=time.ctime(Tem['Start'])
        return Tem
    def delete(self,name): # Stops Log with given Name
        for ind,x in enumerate(TimeKeeper):
            if x['Log'] == name:
                if not ('Stop' in x):
                    x['Stop']=time.time()

class SummaryReport(Resource):
    def __init__(self):
        pass
    def get(self,name): # Gets all the Logs of Provided Name
        FinalReport=[]
        CompleteReport=[]
        TotalDuration=0
        for reports in (TimeKeeper):
            logged=displog(reports)
            CompleteReport.append(logged)
            if reports['Log'] == name:
                FinalReport.append(logged)
                if 'Stop' in logged:
                    timeexpenditure = reports['Stop'] - reports['Start']
                else:
                    timeexpenditure = time.time() - reports['Start']
                TotalDuration+=timeexpenditure
        if len(FinalReport) == 0:
            return CompleteReport
        else:
            return {"Expenditure":timeelapsed(TotalDuration), "Report": name,"Data":FinalReport}

    def delete(self,name): # Clears Everything
        TimeKeeper=[]

api.add_resource(CreateTracker ,'/Track/<string:name>')
api.add_resource(SummaryReport ,'/Summary/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
