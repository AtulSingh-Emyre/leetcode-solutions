import java.util.HashMap;
import java.util.HashSet;

class Solution {
    public TreeNode createBinaryTree(int[][] descriptions) {
        HashMap<Integer, TreeNode> cache = new HashMap<>();
        HashSet<Integer> children = new HashSet<>();
        
        for (int[] d : descriptions) {
            int parent = d[0];
            int child = d[1];
            boolean isLeft = d[2] == 1;
            
            // Java's putIfAbsent skips the conditional check boilerplate
            cache.putIfAbsent(parent, new TreeNode(parent));
            cache.putIfAbsent(child, new TreeNode(child));
            
            if (isLeft) {
                cache.get(parent).left = cache.get(child);
            } else {
                cache.get(parent).right = cache.get(child);
            }
            
            // Track the child node
            children.add(child);
        }
        
        // Find the one key in cache that never acted as a child
        for (int key : cache.keySet()) {
            if (!children.contains(key)) {
                return cache.get(key);
            }
        }
        
        return null;
    }
}
