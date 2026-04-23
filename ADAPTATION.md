# ADAPTATION.md: The KTT Differentiator

## 1. Morning Digest (Feature Phone Strategy)
For users without smartphones or stable 4G, the 24-hour forecast is compressed into 3 mission-critical SMS messages sent at 07:00 AM.

**SMS 1: The Status**
> SENTINEL: Good morning Gabriel. Grid risk is LOW today (8%). Peak risk: 2PM-4PM (45%). 10 appliances active. Reply '1' for the schedule.

**SMS 2: The Action Plan**
> 2PM-4PM ACTION: AC and Water Heater will be SHED. Sewing machine & Lights stay ON. Use charcoal for backup water heating. Stay productive!

**SMS 3: Kinyarwanda Translation**
> SAKWE: Mwiriwe Gabriel. Akazi ni muryohe. Saa 08-10 z'amanywa tuzazimya AC n'icyuma gishushya amazi. Amatara n'imashini bizaguma kwaka. Ngaho akazi keza!

---

## 2. Resilience: Offline "Risk Budget" Protocol
In Kigali, internet fiber or mobile data often drops mid-day. The "Sentinel-Guard" protocol ensures the salon doesn't go dark during a disconnect.

* **UI Display:** The dashboard header switches from Blue to **Amber**. It displays: *"Using Cached Plan (Updated 3h ago). Link Offline."*
* **The Risk Budget:** We allow a maximum **4-hour staleness** window.
    * **Hours 0-2 of Offline:** 100% adherence to the last cached 24-hour JSON plan stored in the local gateway's RAM.
    * **Hours 2-4 of Offline:** The system applies a **10% "Uncertainty Tax"**, lowering the threshold for shedding non-essential items (e.g., shedding the TV at 20% risk instead of 30%).
    * **Hour 4+:** The system enters **Safe-Mode**. It stops trusting the outdated forecast and sheds all "Luxury" and "Comfort" items to protect the breaker until a new heartbeat is received.

---

## 3. Accessibility: The LED Relay Interface
To support users with low literacy or those in a high-speed work environment where reading a screen is impractical, we use a **Physical LED-Status Board** mounted next to the main electrical panel.

### The Solution: Color-Coded LED Relay
* **Solid Green:** System stable. All appliances (including AC/Heaters) are authorized.
* **Solid Yellow:** Outage probability > 20%. Non-essential "Comfort" items (TV/Music) are cut. Staff see the yellow light and know not to restart the AC.
* **Solid Red:** Outage probability > 40%. Only "Critical" tools (Sewing machines/Lights) are powered.
* **Blinking Red:** Immediate grid collapse predicted. Turn off all heavy motors now.

### Justification
In a busy salon, an **ambient information stream** is superior to a digital dashboard. A bright LED requires **zero literacy**, is visible across a crowded room, and provides an immediate, culturally-neutral signal for the entire staff to coordinate their work without needing to check a phone.

---

## 4. Ground Reality Workflow
* **User:** Local Salon Owner in Nyarugenge District.
* **Hardware:** Raspberry Pi Zero (Low power) + 8-Channel Relay Module.
* **Data Footprint:** Heartbeat signals are optimized to < 20KB per refresh to conserve expensive mobile data.
