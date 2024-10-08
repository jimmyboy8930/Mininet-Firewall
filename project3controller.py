# Final Skeleton
#
# Hints:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. 
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.

    myMsg = of.ofp_flow_mod()
    myMsg.match = of.ofp_match.from_packet(packet)
    myMsg.idle_timeout = 60
    myMsg.hard_timeout = 60
    myMsg.data = packet_in
    myMsg.actions = []
    
    ip = packet.find('ipv4')
    ip6 = packet.find('ipv6')
    icmp = packet.find('icmp')

    if not ip: 
      if ip6:
        return
      
      msgAction = of.ofp_action_output(port=of.OFPP_FLOOD)
      myMsg.actions.append(msgAction) 

    # write forward function with code in hint and call that instead   

    else:
      if switch_id != 4:
        if port_on_switch == 1: # from host
          msgAction = of.ofp_action_output(port=3)  # send to s4
          myMsg.actions.append(msgAction)
        
        elif port_on_switch == 3: # from s4
          msgAction = of.ofp_action_output(port=1) # send to host
          myMsg.actions.append(msgAction)

      elif switch_id == 4:
        if port_on_switch == 1: # from h4
          if icmp:
            self.connection.send(myMsg)
            return
          
          elif ip.dstip == '10.5.5.50': # going to h5: blocked
            self.connection.send(myMsg)
            return
          
          # a little redundant but simplest way to deal with packets coming from h4
          elif ip.dstip == '10.1.1.10': # going to h1
            msgAction = of.ofp_action_output(port=4)
            myMsg.actions.append(msgAction)

          elif ip.dstip == '10.2.2.20': # going to h2
            msgAction = of.ofp_action.output(port=5)
            myMsg.actions.append(msgAction)

          elif ip.dstip == '10.3.3.30': # going to h3
            msgAction = of.ofp_action_output(port=6)
            myMsg.actions.append(msgAction)
          
        else: # from anywhere but h4
          if ip.dstip == '123.45.67.89': # going to h4
            msgAction = of.ofp_action.output(port=1)
            myMsg.actions.append(msgAction)
          
          elif ip.dstip == '10.1.1.10': # going to h1
            msgAction = of.ofp_action_output(port=4)
            myMsg.actions.append(msgAction)

          elif ip.dstip == '10.2.2.20': # going to h2
            msgAction = of.ofp_action.output(port=5)
            myMsg.actions.append(msgAction)

          elif ip.dstip == '10.3.3.30': # going to h3
            msgAction = of.ofp_action_output(port=6)
            myMsg.actions.append(msgAction)

          elif ip.dstip == '10.5.5.50': # going to h5
            msgAction = of.ofp_action.output(port=7)
            myMsg.actions.append(msgAction)

    self.connection.send(myMsg)
    return

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
