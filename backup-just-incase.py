from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
    """
    A Firewall object is created for each switch that connects. 
    This object manages packet routing and blocking based on switch connections and IP headers.
    """
    def __init__ (self, connection):
        """
        Initialize the firewall with a connection to the switch.
        """
        self.connection = connection  # Reference to the switch connection to send commands.
        connection.addListeners(self)
              # Register to listen to the PacketIn events.

    def do_final (self, packet, packet_in, port_on_switch, switch_id):
        """
        Handle the processing of packets based on switch and port information.
        """
        myMsg = of.ofp_flow_mod()  # Initialize flow modification message.
        myMsg.match = of.ofp_match.from_packet(packet)  # Set packet matching to the incoming packet.
        myMsg.idle_timeout = 60  # Time after which the flow entry expires if idle.
        myMsg.hard_timeout = 60  # Maximum life of the flow entry.
        myMsg.data = packet_in  # Include the original packet in the flow mod.
        myMsg.actions = []  # Initialize action list for this flow entry.

        ip = packet.find('ipv4')  # Check for IPv4 headers.
        ip6 = packet.find('ipv6')  # Check for IPv6 headers.
        icmp = packet.find('icmp')  # Check for ICMP headers.

        if not ip:  # If there is no IPv4 header.
            if ip6:
                return  # Ignore IPv6 packets.
            # If no IP header is found, flood the packet to all ports.
            msgAction = of.ofp_action_output(port=of.OFPP_FLOOD)
            myMsg.actions.append(msgAction) 

        else:
            # Logic for non-switch 4 scenarios.
            if switch_id != 4:
                if port_on_switch == 1:  # Packet from host connected directly to the switch.
                    msgAction = of.ofp_action_output(port=3)  # Send to s4.
                    myMsg.actions.append(msgAction)

                elif port_on_switch == 3:  # Packet from s4.
                    msgAction = of.ofp_action_output(port=1)  # Send back to the host.
                    myMsg.actions.append(msgAction)

            # Logic specific to switch 4.
            elif switch_id == 4:
                if port_on_switch == 1:  # Packet from h4.
                    if icmp:
                        self.connection.send(myMsg)
                        return

                    elif ip.dstip == '10.5.5.50':  # Going to h5; blocked.
                        self.connection.send(myMsg)
                        return

                    elif ip.dstip == '10.1.1.10':  # Going to h1.
                        msgAction = of.ofp_action_output(port=4)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.2.2.20':  # Going to h2.
                        msgAction = of.ofp_action_output(port=5)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.3.3.30':  # Going to h3.
                        msgAction = of.ofp_action_output(port=6)
                        myMsg.actions.append(msgAction)

                else:  # Packets from anywhere but h4.
                    if ip.dstip == '123.45.67.89':  # Going to h4.
                        msgAction = of.ofp_action_output(port=1)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.1.1.10':  # Going to h1.
                        msgAction = of.ofp_action_output(port=4)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.2.2.20':  # Going to h2.
                        msgAction = of.ofp_action_output(port=5)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.3.3.30':  # Going to h3.
                        msgAction = of.ofp_action_output(port=6)
                        myMsg.actions.append(msgAction)

                    elif ip.dstip == '10.5.5.50':  # Going to h5.
                        msgAction = of.ofp_action_output(port=7)
                        myMsg.actions.append(msgAction)

        self.connection.send(myMsg)  # Send the flow mod message to the switch.
        return

    def _handle_PacketIn (self, event):
        """
        Process PacketIn events that occur when the switch forwards a packet to the controller.
        """
        packet = event.parsed  # The parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")  # Log and ignore incomplete packets.
            return

        packet_in = event.ofp  # The actual OpenFlow packet-in message.
        self.do_final(packet, packet_in, event.port, event.dpid)  # Process the packet.

def launch ():
    """
    Launches the controller application.
    """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        Final(event.connection)  # Create a Final instance for each switch connection.

    core.openflow.addListenerByName("ConnectionUp", start_switch)  # Listen for switch connections.
