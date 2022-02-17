log_file = "logfile.log"

while [ 1 ]
do
	echo "--------------------" >> $log_file
	date "+%Y-%m%d %T" >> $log_file
	echo "--------------------" >> $log_file

	git pull

	python asaRunThisOnYour.py >> $log_file

	# TODO:
	# - Test if changes have been made using `git status`
	# - If changes have been made
	# -- git add
	# -- git commit
	# -- git push
done
