# awx-test

Steps required for this task are:
I created a number of virtual machines. Each instance must have passwordless SSH access,
for the automation to work. To achieve this, provision each instance with a cloud-init
manifest that imports the current users' public SSH key and into a user microk8s.
The scirp creates a Ubuntu 22.04 based vm with 4 cpus, 8GB ram and 20GB disk space.

This script is responsible for the tasks above: tools/multipass_create_instances.sh

The tools/multipass_generate_inventory.py scripts generates the inventory.yml file
to use, as Ansible works against multiple managed nodes or “hosts” in the infrastructure
at the same time, using a list or group of lists known as inventory. Once the inventory
is defined, we can use patterns to select the hosts or groups we want Ansible to run against.

Since we have our clusters running, the site.yml file with the inventory file provisions
the nodes: ansible-playbook site.yml -i tools/inventory.yml

It installed the following services for all of the nodes: microk8s, docker.

For the worker nodes Helm and the AWX services are installed.

Since I was working on M1 macbook with arm64 cpu I tried several time but it was not possible
to enbale awx operator on the node's kubernetes cluster. The pod did come up but it went
immediately to a CrashBackLoop state, for several hours I tried to figure it how to fix it
but I could not unfortunately, I'm sorry about that.

However I managed to install it on my own laptop running a kubernetes cluster and with Kustomize.

These were the steps for it:

First, created a file called kustomization.yaml.
Installed the manifests by running this: kustomize build . | kubectl apply -f -
Create a file named awx-demo.yaml.
Added this new file to the list of "resources" in the kustomization.yaml file.
Created the AWX instance in the cluster: kustomize build . | kubectl apply -f -
Started the service: minikube service awx-demo-service --url
Retrieved the admin password: kubectl get secret awx-demo-admin-password -o jsonpath="{.data.password}" | base64 --decode
After this the AWX can be reached from localhost

To set up a test project and test jobs I used cli commands:

export TOWER_OAUTH_TOKEN=aZ0ZNAadBvHi4CX9S01bjhPBIeM94H
export TOWER_HOST=http://127.0.0.1:52943
$(TOWER_USERNAME=admin TOWER_PASSWORD=uJLLr7pFWX7KSxBskJcP5JVpl7q9WyJW awx login -f human)
awx config
awx projects create --wait --organization 1 --name='Example Project' --scm_type git --scm_url 'https://github.com/ansible/ansible-tower-samples' -f human
awx job_templates create --name='Example Job Template' --project 'Example Project' --playbook hello_world.yml --inventory 'Demo Inventory' -f human
awx job_templates launch 'Example Job Template' --monitor -f human
------Starting Standard Out Stream------

PLAY [Hello World Sample] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Hello Message] ***********************************************************
ok: [localhost] => {
    "msg": "Hello World!"
}

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
------End of Standard Out Stream--------

id name                 
== ==================== 
3  Example Job Template

