
import random
import heapq
import ipaddress

from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.link import TCLink


def CreateNetwork(router_count, host_count, extra_links=0, seed=None):
    if not 2 <= router_count <= 254:
        raise ValueError("router_count must be between 2 and 254")
    if host_count < 1:
        raise ValueError("host_count must be positive")

    rng = random.Random(seed)

    net = Mininet(
        topo=None,
        build=False,
        controller=None,
        switch=OVSSwitch,
        link=TCLink
    )

    # Create routers and their LAN switches
    routers = []
    switches = []
    lan_links = []

    for i in range(router_count):
        r = net.addHost(f"r{i+1}", cls=Node, ip="0.0.0.0")
        s = net.addSwitch(f"s{i+1}", failMode="standalone")

        link = net.addLink(r, s, delay="0.5ms")

        routers.append(r)
        switches.append(s)
        lan_links.append(link)

    # Connected ring of routers
    edges = {
        tuple(sorted((i, (i + 1) % router_count)))
        for i in range(router_count)
        if i != (i + 1) % router_count
    }

    # Add random extra connections
    possible = [
        (i, j)
        for i in range(router_count)
        for j in range(i + 1, router_count)
        if (i, j) not in edges
    ]

    if extra_links > len(possible) or extra_links < 0:
        raise ValueError("Invalid extra_links count")

    edges.update(rng.sample(possible, extra_links))

    # Each router-to-router link gets a /30 subnet
    subnets = ipaddress.IPv4Network("172.16.0.0/12").subnets(
        new_prefix=30
    )

    graph = {i: [] for i in range(router_count)}
    router_links = []

    for a, b in sorted(edges):
        subnet = next(subnets)
        ip_a, ip_b = [str(ip) for ip in subnet.hosts()]
        delay = rng.uniform(2, 20)

        link = net.addLink(
            routers[a],
            routers[b],
            delay=f"{delay:.2f}ms"
        )

        router_links.append((a, b, link, ip_a, ip_b))

        graph[a].append((b, delay, ip_b, link.intf1.name))
        graph[b].append((a, delay, ip_a, link.intf2.name))

    # Randomly attach hosts to router LANs
    hosts = []
    host_links = []
    counts = [0] * router_count

    for i in range(host_count):
        r = rng.randrange(router_count)
        counts[r] += 1

        if counts[r] > 65533:
            raise ValueError("Too many hosts on one LAN")

        subnet = ipaddress.IPv4Network(f"10.{r+1}.0.0/16")
        ip = str(subnet.network_address + counts[r] + 1)

        h = net.addHost(f"h{i+1}", ip=f"{ip}/16")
        link = net.addLink(h, switches[r], delay="0.5ms")

        hosts.append(h)
        host_links.append((h, r, link, ip))

    # Start Mininet
    net.build()
    net.start()

    # Configure router LAN interfaces
    for i, router in enumerate(routers):
        router.setIP(
            f"10.{i+1}.0.1/16",
            intf=lan_links[i].intf1
        )

        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.cmd("sysctl -w net.ipv4.conf.all.rp_filter=0")
        router.cmd("sysctl -w net.ipv4.conf.default.rp_filter=0")

    # Configure inter-router interfaces
    for a, b, link, ip_a, ip_b in router_links:
        routers[a].setIP(f"{ip_a}/30", intf=link.intf1)
        routers[b].setIP(f"{ip_b}/30", intf=link.intf2)

    # Configure host interfaces and default gateways
    for h, r, link, ip in host_links:
        h.setIP(f"{ip}/16", intf=link.intf1)
        h.cmd(f"ip route replace default via 10.{r+1}.0.1")

    # Dijkstra: install shortest-delay routes to each LAN
    for source in range(router_count):
        distances = {source: 0}
        first_hop = {}
        queue = [(0, source)]

        while queue:
            dist, current = heapq.heappop(queue)

            if dist > distances[current]:
                continue

            for neighbor, delay, next_ip, intf in graph[current]:
                new_dist = dist + delay

                if new_dist < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_dist

                    first_hop[neighbor] = (
                        (next_ip, intf)
                        if current == source
                        else first_hop[current]
                    )

                    heapq.heappush(queue, (new_dist, neighbor))

        for dest in range(router_count):
            if dest == source:
                continue

            next_ip, intf = first_hop[dest]

            routers[source].cmd(
                f"ip route replace 10.{dest+1}.0.0/16 "
                f"via {next_ip} dev {intf}"
            )

    print(f"Created {router_count} routers, {host_count} hosts")
    print(f"Inter-router links: {len(edges)}")

    return net, hosts
