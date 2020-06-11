from chronos.trigger import IntervalTrigger, OnStartupTrigger

interval_trigger = IntervalTrigger(
    1000
)  # Register interval trigger with a tick time of 100ms, the trigger is driven by the main clock
on_startup_trigger = OnStartupTrigger()
