def format_alert_summary(alert_count, severity):
	return "There are " + str(alert_count) + " " + severity + " alerts active."
 
 
def get_alert_owner(alert, team_directory):
	return team_directory.get(alert["owner"], "Unassigned")
 
 
def average_response_time(response_times):
	count = len(response_times)
	if count == 0:
		return 0.0
	return sum(response_times) / count
