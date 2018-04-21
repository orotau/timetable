import collections
day_chunk = collections.namedtuple("day_chunk", "day start end title")

day_chunks = []
#Monday
day_chunks.append(day_chunk("Monday", "08:45:00", "09:55:00", "Period 1"))
day_chunks.append(day_chunk("Monday", "09:55:00", "10:50:00", "Period 2"))
day_chunks.append(day_chunk("Monday", "11:45:00", "12:40:00", "Period 3"))
day_chunks.append(day_chunk("Monday", "12:40:00", "13:35:00", "Period 4"))
day_chunks.append(day_chunk("Monday", "14:10:00", "15:05:00", "Period 5"))

#Tuesday
day_chunks.append(day_chunk("Tuesday", "08:45:00", "10:00:00", "Period 1"))
day_chunks.append(day_chunk("Tuesday", "10:00:00", "11:00:00", "Period 2"))
day_chunks.append(day_chunk("Tuesday", "11:45:00", "12:40:00", "Period 3"))
day_chunks.append(day_chunk("Tuesday", "12:40:00", "13:35:00", "Period 4"))
day_chunks.append(day_chunk("Tuesday", "14:10:00", "15:05:00", "Period 5"))

#Wednesday
day_chunks.append(day_chunk("Wednesday", "09:25:00", "10:25:00", "Period 1"))
day_chunks.append(day_chunk("Wednesday", "10:25:00", "11:20:00", "Period 2"))
day_chunks.append(day_chunk("Wednesday", "11:45:00", "12:40:00", "Period 3"))
day_chunks.append(day_chunk("Wednesday", "12:40:00", "13:35:00", "Period 4"))
day_chunks.append(day_chunk("Wednesday", "14:10:00", "15:05:00", "Period 5"))

#Thursday
day_chunks.append(day_chunk("Thursday", "08:45:00", "10:00:00", "Period 1"))
day_chunks.append(day_chunk("Thursday", "10:00:00", "11:00:00", "Period 2"))
day_chunks.append(day_chunk("Thursday", "11:45:00", "12:40:00", "Period 3"))
day_chunks.append(day_chunk("Thursday", "12:40:00", "13:35:00", "Period 4"))
day_chunks.append(day_chunk("Thursday", "14:10:00", "15:05:00", "Period 5"))

#Friday
day_chunks.append(day_chunk("Friday", "08:45:00", "09:55:00", "Period 1"))
day_chunks.append(day_chunk("Friday", "09:55:00", "10:50:00", "Period 2"))
day_chunks.append(day_chunk("Friday", "11:45:00", "12:40:00", "Period 3"))
day_chunks.append(day_chunk("Friday", "12:40:00", "13:35:00", "Period 4"))
day_chunks.append(day_chunk("Friday", "14:10:00", "15:05:00", "Period 5"))

