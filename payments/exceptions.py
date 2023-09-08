class ReservationTimeOut(ValueError):
    def __str__(self) -> str:
        return "The reservation is timeout because it spent over 10 minutes."