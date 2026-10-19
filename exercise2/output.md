kubectl get deployments  
NAME        READY   UP-TO-DATE   AVAILABLE   AGE  
flask-app   1/1     1            1           7s  

kubectl get services  
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE  
flask-app-service   NodePort    10.97.196.21    <none>        15000:31103/TCP   6s  
hello-k8s           NodePort    10.102.41.222   <none>        80:30714/TCP      122m  
kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP           124m  


kubectl get pods -l app=flask-app  
NAME                         READY   STATUS    RESTARTS   AGE  
flask-app-59f7cdccb4-s9m2h   1/1     Running   0          16s  

curl http://127.0.0.1:44851  
Hello from Flask on Kubernetes!  