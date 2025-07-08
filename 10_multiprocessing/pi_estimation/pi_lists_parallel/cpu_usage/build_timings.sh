rm *.pickle
rm *.png
python profile_cpu_usage.py --processes --nbr_processes=16 --build
python profile_cpu_usage.py --processes --nbr_processes=8 --build
python profile_cpu_usage.py --processes --nbr_processes=4 --build
python profile_cpu_usage.py --processes --nbr_processes=2 --build
python profile_cpu_usage.py --processes --nbr_processes=1 --build
python profile_cpu_usage.py --nbr_processes=8 --build

