"""
Graph differ — compares two NetworkX DiGraphs and reports what changed.

Uses simple set math:
  - added   = in head but not in base
  - removed = in base but not in head
  - modified = same node ID but attributes changed
  - newly_exposed / no_longer_exposed = internet edge changes
  - exposure_delta = net change in public edges
"""

import networkx as nx


def diff_graphs(base: nx.DiGraph, head: nx.DiGraph) -> dict:
    """
    Compare a base graph and a head graph.

    Returns a dict with:
      - added_nodes:       resource IDs new in head
      - removed_nodes:     resource IDs deleted from base
      - added_edges:       edge dicts new in head
      - removed_edges:     edge dicts gone from base
      - modified_nodes:    resource IDs present in both but with changed attributes
      - newly_exposed:     resources that gained an internet → X edge
      - no_longer_exposed: resources that lost an internet → X edge
      - exposure_delta:    count of public edges added minus removed
    """
    base_node_ids = set(base.nodes)
    head_node_ids = set(head.nodes)

    added_nodes = sorted(head_node_ids - base_node_ids)
    removed_nodes = sorted(base_node_ids - head_node_ids)

    # --- Modified nodes (same ID, different attributes) ---
    common_nodes = base_node_ids & head_node_ids
    modified_nodes = sorted(
        nid for nid in common_nodes
        if dict(base.nodes[nid]) != dict(head.nodes[nid])
    )

    # --- Edge diffs ---
    base_edge_set = set(base.edges)
    head_edge_set = set(head.edges)

    added_edge_tuples = sorted(head_edge_set - base_edge_set)
    removed_edge_tuples = sorted(base_edge_set - head_edge_set)

    added_edges = [
        {
            "source": src,
            "target": tgt,
            **{k: v for k, v in head.edges[src, tgt].items()},
        }
        for src, tgt in added_edge_tuples
    ]

    removed_edges = [
        {
            "source": src,
            "target": tgt,
            **{k: v for k, v in base.edges[src, tgt].items()},
        }
        for src, tgt in removed_edge_tuples
    ]

    # --- Internet exposure detection ---
    base_internet_targets = {
        tgt for src, tgt in base.edges if src == "internet"
    }
    head_internet_targets = {
        tgt for src, tgt in head.edges if src == "internet"
    }

    newly_exposed = sorted(head_internet_targets - base_internet_targets)
    no_longer_exposed = sorted(base_internet_targets - head_internet_targets)

    # --- Exposure delta (net change in public edges) ---
    base_public = sum(
        1 for _, _, d in base.edges(data=True)
        if d.get("exposure_type") == "public"
    )
    head_public = sum(
        1 for _, _, d in head.edges(data=True)
        if d.get("exposure_type") == "public"
    )
    exposure_delta = head_public - base_public

    return {
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "added_edges": added_edges,
        "removed_edges": removed_edges,
        "modified_nodes": modified_nodes,
        "newly_exposed": newly_exposed,
        "no_longer_exposed": no_longer_exposed,
        "exposure_delta": exposure_delta,
    }
