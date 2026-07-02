from alerts.alert import Alert

class ManyPlantsAlert(Alert):

    def update(self, data):
        print("Plants occupy more than 90% of grid")
