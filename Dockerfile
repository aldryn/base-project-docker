FROM aldryn/base:2.1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
ADD generated_requirements.txt /app/
RUN pip install --use-wheel -r requirements.txt
ADD . /app/
EXPOSE 80
ENV PORT 80
CMD ["/app/launcher.sh"]
