annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl get pods  
NAME                 READY   STATUS    RESTARTS   AGE  
flashsale-rs-2nxf7   1/1     Running   0          9s  
flashsale-rs-4bxmt   1/1     Running   0          9s  
flashsale-rs-rtszh   1/1     Running   0          9s  
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl scale rs flashsale-rs --replicas=5
replicaset.apps/flashsale-rs scaled  
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl get pods  
NAME                 READY   STATUS    RESTARTS   AGE  
flashsale-rs-2nxf7   1/1     Running   0          35s  
flashsale-rs-4bxmt   1/1     Running   0          35s  
flashsale-rs-8cw2s   1/1     Running   0          12s  
flashsale-rs-rtszh   1/1     Running   0          35s  
flashsale-rs-tbpmz   1/1     Running   0          12s  
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl delete pod flashsale-rs-2nxf7 
pod "flashsale-rs-2nxf7" deleted from default namespace    
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl get pods  
NAME                 READY   STATUS    RESTARTS   AGE  
flashsale-rs-4bxmt   1/1     Running   0          90s  
flashsale-rs-5lkxk   1/1     Running   0          11s  
flashsale-rs-8cw2s   1/1     Running   0          67s  
flashsale-rs-rtszh   1/1     Running   0          90s  
flashsale-rs-tbpmz   1/1     Running   0          67s  
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl get pods -o wide  
NAME                 READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES  
flashsale-rs-4bxmt   1/1     Running   0          100s   10.244.0.9    minikube   <none>           <none>  
flashsale-rs-5lkxk   1/1     Running   0          21s    10.244.0.13   minikube   <none>           <none>  
flashsale-rs-8cw2s   1/1     Running   0          77s    10.244.0.11   minikube   <none>           <none>  
flashsale-rs-rtszh   1/1     Running   0          100s   10.244.0.10   minikube   <none>           <none>  
flashsale-rs-tbpmz   1/1     Running   0          77s    10.244.0.12   minikube   <none>           <none>  
annieunix@DESKTOP-UBU709H:~/devops/exercise3$ kubectl get rs  
NAME           DESIRED   CURRENT   READY   AGE  
flashsale-rs   5         5         5       33m  