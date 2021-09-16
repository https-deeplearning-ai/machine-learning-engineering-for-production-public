DO 
{curl.exe -d '{\"instances\": [1.0, 2.0, 5.0]}' -X POST "$(minikube ip):30001/v1/models/half_plus_two:predict"
} WHILE(1)