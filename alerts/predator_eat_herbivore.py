from alerts.alert import Alert

class PredatorEatHerbivoreAlert(Alert):

    def update(self, data):
        print("A predator ate a herbivore")
        