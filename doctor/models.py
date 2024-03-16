from django.db import models

from utils.models import BaseModel


class DoctorProfile(BaseModel):
    full_name = models.CharField(max_length=255)


class Slot(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class TimeSlot(BaseModel):
    from_time = models.TimeField()
    to_tiem = models.TimeField()
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="time_slot")
