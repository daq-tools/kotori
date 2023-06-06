# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl <andreas@getkotori.org>
import pytest

from kotori.daq.strategy.wan import WanBusStrategy
from kotori.util.common import SmartMunch


@pytest.mark.strategy
def test_wan_strategy_wide_channel():
    """
    Verify the classic WAN topology decoding, using a channel-based addressing scheme.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/acme/area-42/foo-70b3d57ed005dac6/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "acme",
            "gateway": "area-42",
            "node": "foo-70b3d57ed005dac6",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_generic_success():
    """
    Verify the per-device WAN topology decoding, using a generic device identifier.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/device/123e4567-e89b-12d3-a456-426614174000/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "devices",
            "gateway": "default",
            "node": "123e4567-e89b-12d3-a456-426614174000",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_basic():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier, which translates to the topology.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/acme-area42-eui70b3d57ed005dac6/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "acme",
            "gateway": "area42",
            "node": "eui70b3d57ed005dac6",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_too_few_components():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier with too few components.
    The solution is to pad the segments with `default` labels at the front.

    This specific test uses a vanilla TTN device identifier.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/eui-70b3d57ed005dac6/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "default",
            "gateway": "eui",
            "node": "70b3d57ed005dac6",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_three_components():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier with exactly three components.
    This topic will be decoded as-is.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/acme-area42-eui70b3d57ed005dac6/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "acme",
            "gateway": "area42",
            "node": "eui70b3d57ed005dac6",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_too_many_components_merge_suffixes():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier with too many components.
    The solution is to merge all trailing segments into the `node` slot, re-joining them with `-`.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/acme-area42-eui70b3d57ed005dac6-suffix/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "acme",
            "gateway": "area42",
            "node": "eui70b3d57ed005dac6-suffix",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_too_many_components_redundant_realm():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier with too many components.

    This is an edge case where the first addressing component actually equals the realm.
    Strictly, it is a misconfiguration, but we pretend to be smart, and ignore that,
    effectively not using the redundant information, and ignoring the `myrealm-` prefix
    within the device identifier slot altogether.

    Cheers, @thiasB.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/myrealm-acme-area42-eui70b3d57ed005dac6/data.json")
    assert topology == SmartMunch(
        {
            "realm": "myrealm",
            "network": "acme",
            "gateway": "area42",
            "node": "eui70b3d57ed005dac6",
            "slot": "data.json",
        }
    )


@pytest.mark.strategy
def test_wan_strategy_device_generic_empty():
    """
    Verify the per-device WAN topology decoding, using a generic device identifier with no components.
    Topic-to-topology decoding should return `None`.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/device/data.json")
    assert topology is None


@pytest.mark.strategy
def test_wan_strategy_device_dashed_topo_empty():
    """
    Verify the per-device WAN topology decoding, using a dashed device identifier with no components.
    Topic-to-topology decoding should return `None`.
    """
    strategy = WanBusStrategy()
    topology = strategy.topic_to_topology("myrealm/channel/data.json")
    assert topology is None
