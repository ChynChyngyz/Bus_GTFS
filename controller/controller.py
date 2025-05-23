from model import Model
from view import View
from PyQt5.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.view = View(self)
        self.model = Model(self)
        self.view.disableModes(self.model.workspace.getPossibleModes())
        self.reloadStops()
        self.exec_()

    def askNewWorkspace(self, path = '~', confirm = False): return self.view.askNewWorkspace(path, confirm)
    def askInitWorkspace(self): return self.view.askInitWorkspace()
    def askInitWorkspaceParameters(self, lat, lon, r): return self.view.askInitWorkspaceParameters(lat, lon, r)
    def showLoading(self, txt): return self.view.showLoading(txt)
    def showError(self, txt): return self.view.showError(txt)

    def reloadStops(self, modes = [0, 1, 2, 3, 4, 5, 6, 7]):
        names, ids, lats, lons, types = self.model.workspace.getAllStops(modes)
        self.view.drawStops(lats, lons, types)
        self.view.fillStopSelectors(ids, names)

    def drawStopPath(self, path, withStopTimes = False):
        names, ids, lats, lons, types, rnames, rcols = self.model.workspace.getStopsByStopIds(path)
        self.view.drawStopPath(lats, lons)
        if withStopTimes != False: self.view.fillResultTable(withStopTimes, names, types, rnames, rcols)

    def runShortestPath(self, modes, params):
        stop_ids, stop_times = self.model.dijkstra(params['from_stop_id'], params['departure_time'], params['to_stop_id'], modes)
        self.drawStopPath(stop_ids, stop_times)

    def changeWorkspace(self, default, confirm = False):
        self.model.changeWorkspace('~', confirm)
        self.view.disableModes(self.model.workspace.getPossibleModes())
        self.reloadStops()
