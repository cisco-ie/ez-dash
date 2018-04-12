# ez-dash
**Dashboarding with Open-Source Monitoring Stacks Made Easy**  
*DevNet Create 2018 - WS23, WS54* | [Presentation](Dashboarding%20with%20Open-Source%20Monitoring%20Stacks%20Made%20Easy.pptx)

Learn about the different open source tools like TICK, ELK, Prometheus, Grafana, and more - and how to make good looking dashboards of your environment without having to rebuild the wheel.

* [Objectives](#objectives)
* [Prerequisites](#prerequisites)
  * [Install Docker CE](#install-docker-ce)
  * [Get the code!](#get-the-code)
* [Help!](#help)

## Objectives

* Provide a quick introduction to monitoring concepts
* Provide a quick introduction to available tooling
* Create a sample environment/application which exposes metrics to monitoring tooling
* Explore sample dashboards in Grafana
* Create custom dashboards in Grafana

## Prerequisites
In order to complete this lab you will need a development workstation with Docker, and other fundamental tools installed. :)

* [Docker [CE]](https://www.docker.com/community-edition)
  * Community Edition is fully capable.
  * v17.06 or higher.
* Web browser
  * Latest versions of most browsers work.
  * [Firefox](https://www.mozilla.org/en-US/firefox/developer/) or [Chrome](https://www.google.com/chrome/) recommended.

### Install Docker CE

* [Mac OS[X]](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) / [Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
* [CentOS](https://docs.docker.com/install/linux/docker-ce/centos/) / [Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)

### Get the code!
* If you have `git` installed...  
`git clone https://github.com/cisco-ie/ez-dash`
* Otherwise, [download](https://github.com/cisco-ie/ez-dash/archive/master.zip) from your web browser or other tool.  
https://github.com/cisco-ie/ez-dash/archive/master.zip

You're ready to workshop!

## Usage
This stack should work across any OS that supports the prerequisited Docker CE installation. All processes are containerized and deployable via Docker Swarm. If you are running pre-existing Docker containers, ensure that there are no port conflicts in the `docker-compose.yml` file.

Explanation of the components is provided in the [Dashboarding with Open-Source Monitoring Stacks Made Easy](Dashboarding%20with%20Open-Source%20Monitoring%20Stacks%20Made%20Easy.pptx) PowerPoint.

### Get Started
The following expects you to utilize a terminal of some kind, also known as command prompt in Windows.

```bash
# Get the code!
git clone https://github.com/cisco-ie/ez-dash
cd ez-dash
# If you have never run Docker Swarm before...
./setup.sh # MacOS or Linux
.\setup.bat # Windows
# Start the stack!
./start.sh # MacOS or Linux
.\start.bat # Windows
# See what's running!
docker stack ps ezdash
# Shut it down when you're done!
./stop.sh # MacOS or Linux
.\stop.bat # Windows
```

### Web Interfaces
The following listings detail ports made available over HTTP to explore the stack.

* Grafana
  * http://localhost:3000/
  * Credentials: `admin/admin`
* Kibana
  * http://localhost:5601/
* Prometheus Query Interface
  * http://localhost:9090/
* Python Application
  * http://localhost:5000/
  * http://localhost:5000/up
  * http://localhost:5000/down
    * Increment/decrement a counter displayed in Grafana and exposed by Prometheus.
  * http://localhost:9091/
    * See Python Application statistics exposed to Prometheus.



## Help!
If you require any assistance, please open an issue in this repository, or reach out to:
* [Karthik Kumaravel](https://github.com/skkumaravel) - [Email](mailto:kkumara3@cisco.com)
* [Remington Campbell](https://github.com/remingtonc) - [Email](mailto:remcampb@cisco.com)
