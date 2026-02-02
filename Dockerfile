ARG IMAGE=containers.intersystems.com/intersystems/iris-community:latest-cd
FROM $IMAGE

COPY . /irisdev/app

# Update environment variables
ENV LD_LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:/home/irisowner/irissys/:${LD_LIBRARY_PATH}
ENV PATH=/home/irisowner/.local/bin:$PATH
ENV IRISNAMESPACE="IRISAPP"

RUN pip3 install -r /irisdev/app/requirements.txt --break-system-packages
