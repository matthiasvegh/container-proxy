# container-proxy
Tool for running programs outside of a the invoking container

## Motivation
When running GUI programs inside a container, it is useful to be able to open
hyperlinks from within that program with a program external to the container.

This can be achieved by creating a symbolic link to `client.py` called
`xdg-open` inside the container, running `server.py`, and mounting the socket
into the container.

## Use with Vagga
[Vagga](https://github.com/talihook/vagga) is a container-runtime that unlike
Docker, does not require running a daemon as root. Configuration would like like
so:

```yaml
containers:
  test:
    setup:
      - !Ubuntu xenial
      - !UbuntuUniverse
      - !Install [python3]
      - !Copy
        source: /work/container_proxy
        path: /usr/lib/python3/dist-packages/container_proxy
      - !Copy
        source: /work/client.py
        path: /usr/bin/xdg-open
    volumes:
      /tmp: !Tmpfs
        size: 100Mi
        mode: 0o1777
        subdirs:
          .X11-unix: #
        files:
          container_proxy.sock: ""
      /tmp/.X11-unix: !BindRW /volumes/X11
      /tmp/container_proxy.sock: !BindRW /volumes/container_proxy_sock
commands:
  run: !Command
    description: "Run program"
    container: test
    work-dir: /work
    run: [bash]
```

Where `X11` and `container_proxy_sock` are
[external volumes](http://vagga.readthedocs.io/en/latest/settings.html#opt-external-volumes)
defined as follows:

```yaml
external-volumes:
  X11: /tmp/.X11-unix
  container_proxy_sock: /tmp/container_proxy.sock
```

When the container launches `xdg-open` due to clicking a hyperlink, the
container will actually run our proxy script that requests the server to launch
the browser for us.
