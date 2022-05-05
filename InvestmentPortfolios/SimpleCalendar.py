class SimpleCalendar:
    SUN = "Sunday"
    MON = "Monday"
    TUE = "Tuesday"
    WED = "Wednesday"
    THU = "Thursday"
    FRI = "Friday"
    SAT = "Saturday"
    __today: str = SUN

    @staticmethod
    def get_today():
        return SimpleCalendar.__today

    @staticmethod
    def eod():
        match SimpleCalendar.__today:
            case SimpleCalendar.SUN:
                SimpleCalendar.__today = SimpleCalendar.MON
            case SimpleCalendar.MON:
                SimpleCalendar.__today = SimpleCalendar.TUE
            case SimpleCalendar.TUE:
                SimpleCalendar.__today = SimpleCalendar.WED
            case SimpleCalendar.WED:
                SimpleCalendar.__today = SimpleCalendar.THU
            case SimpleCalendar.THU:
                SimpleCalendar.__today = SimpleCalendar.FRI
            case SimpleCalendar.FRI:
                SimpleCalendar.__today = SimpleCalendar.SAT
            case SimpleCalendar.SAT:
                SimpleCalendar.__today = SimpleCalendar.SUN
