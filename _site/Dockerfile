FROM bitnami/minideb:latest
Label MAINTAINER Amir Pourmand
RUN apt-get update -y
# add locale
RUN apt-get -y install locales
# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

# add ruby and jekyll
RUN apt-get install --no-install-recommends -y \
    ruby-full \
    build-essential \
    zlib1g-dev \
    ca-certificates \
    curl \
    wget \
    gnupg \
    python3 \
    python3-dev \
    pkg-config \
    libssl-dev \
    libgmp-dev \
    ninja-build \
    clang \
    imagemagick \
    xz-utils \
    unzip \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/
    
# Install additional packages that help building V8/libv8 (used by mini_racer)
RUN apt-get update -y && apt-get install --no-install-recommends -y \
    g++-multilib \
    libc++-dev \
    libc++abi-dev \
    libgtk-3-dev \
    libasound2-dev \
    libx11-dev \
    libx11-xcb-dev \
    libv8-dev || true \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/
# ENV GEM_HOME='root/gems' \
#     PATH="root/gems/bin:${PATH}"
RUN gem install jekyll bundler
RUN mkdir /srv/jekyll
ADD Gemfile /srv/jekyll
WORKDIR /srv/jekyll
RUN bundle install