FROM tutum/buildstep
EXPOSE 80
ENV PORT 80
CMD ["/start", "web"]
