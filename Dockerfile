FROM python:3.7

RUN apt-get update && \
    apt-get install -y cmake build-essential wget unzip

WORKDIR /app

# VOLUME /mnt/home/miyoung/suehyun/cc_net

COPY . /app

# COPY ./Makefile /app/Makefile
# COPY ./setup.py /app/setup.py

RUN mkdir /app/data

RUN apt-get install libeigen3-dev libboost-all-dev -y
RUN make install
RUN pip install .[getpy]
RUN wget -O - https://kheafield.com/code/kenlm.tar.gz | tar -xz && \
    cd kenlm && rm -rf build && mkdir -p build && cd build && cmake .. && make -j2 && \
    mv bin/lmplz bin/build_binary /app/bin && \
    wget -c -O /app/third_party/sentencepiece.zip https://github.com/google/sentencepiece/archive/v0.1.83.zip && \
    unzip -o -d /app/third_party /app/third_party/sentencepiece.zip && \
    mv /app/third_party/sentencepiece-* /app/third_party/sentencepiece && \
    cd /app/third_party/sentencepiece && mkdir -p build && cd build && cmake .. && make -j2 && \
    mv src/spm_train src/spm_encode /app/bin && \
    rm -r /app/kenlm /app/third_party/sentencepiece.zip /root/.cache

RUN apt-get remove -y build-essential && apt-get autoremove -y

CMD ["bash"]
