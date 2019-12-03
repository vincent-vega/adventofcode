import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Stream;

public class Day03
{
    enum Direction {
        UP_R,
        UP_L,
        DOWN_R,
        DOWN_L
    };

    private static long getManhattanDistance(int x1, int y1, int x2, int y2)
    {
        return Math.abs(x1 - x2) + Math.abs(y1 - y2);
    }

    private class WireMap
    {
        private class Coordinate
        {
            int x, y;

            public Coordinate(int x, int y)
            {
                this.x = x;
                this.y = y;
            }

            @Override
            public boolean equals(Object o) { return o != null && ((Coordinate) o).x == x && ((Coordinate) o).y == y; }

            @Override
            public int hashCode() { return String.format("%d|%d", x, y).hashCode(); }
        }

        List<Coordinate> visitedCoords = new ArrayList<>();
        Map<Coordinate, Boolean> map = new HashMap<>();
        int curX = 1, curY = 1;

        public void set(String s)
        {
            int n = Integer.valueOf(s.substring(1));
            switch (s.charAt(0)) {
            case 'L':
                for (int i = 0; i < n; i++)
                    set(curX - 1, curY);
                break;
            case 'R':
                for (int i = 0; i < n; i++)
                    set(curX + 1, curY);
                break;
            case 'U':
                for (int i = 0; i < n; i++)
                    set(curX, curY + 1);
                break;
            case 'D':
                for (int i = 0; i < n; i++)
                    set(curX, curY - 1);
                break;
            default:
                throw new IllegalArgumentException("Invalid map value");
            }
        }

        private void set(int x, int y)
        {
            map.put(new Coordinate(x, y), true);
            visitedCoords.add(new Coordinate(x, y));
            if (x != curX)
                curX = x > curX ? curX + 1 : curX - 1;
            else if (y != curY)
                curY = y > curY ? curY + 1 : curY - 1;
        }

        public boolean checkXSect(int x, int y)
        {
            return x == 1 && y == 1 ? false : map.containsKey(new Coordinate(x, y));
        }

        public int getStepsTo(int x, int y)
        {
            int steps = 0;
            for (Day03.WireMap.Coordinate c : visitedCoords) {
                steps++;
                if (c.x == x && c.y == y)
                    return steps;
            }
            throw new IllegalArgumentException("Invalid coordinates");
        }
    }

    private class CoordinateGenerator implements Iterable<Integer[]>
    {
        int x = 1, y = 2;
        Direction curDir = Direction.DOWN_R;
        int count = 1, size = 1;

        private void reset()
        {
            x = 1;
            y = ++size;
            curDir = Direction.DOWN_R;
        }

        private void changeDir()
        {
            if (curDir.equals(Direction.DOWN_R))
                curDir = Direction.DOWN_L;
            else if (curDir.equals(Direction.DOWN_L))
                curDir = Direction.UP_L;
            else if (curDir.equals(Direction.UP_L))
                curDir = Direction.UP_R;
            else if (curDir.equals(Direction.UP_R))
                reset();
            count = size;
        }

        private void updateCoord()
        {
            if (--count == 0)
                changeDir();
            else {
                if (curDir.equals(Direction.DOWN_R) || curDir.equals(Direction.UP_R)) {
                    x++;
                    y = curDir.equals(Direction.DOWN_R) ? y - 1 : y + 1;
                } else if (curDir.equals(Direction.DOWN_L) || curDir.equals(Direction.UP_L)) {
                    x--;
                    y = curDir.equals(Direction.DOWN_L) ? y - 1 : y + 1;
                }
            }
        }

        @Override
        public Iterator<Integer[]> iterator()
        {
            return new Iterator<Integer[]>()
            {
                @Override
                public boolean hasNext()
                {
                    return true;
                }

                @Override
                public Integer[] next()
                {
                    Integer[] ret = new Integer[] { x, y };
                    updateCoord();
                    return ret;
                }
            };
        }
    }

    public String part1(WireMap m1, WireMap m2)
    {
        Iterator<Integer[]> it = new CoordinateGenerator().iterator();
        while (it.hasNext()) {
            Integer[] idx = it.next();
            if (m1.checkXSect(idx[0], idx[1]) && m2.checkXSect(idx[0], idx[1]))
                return String.valueOf(getManhattanDistance(1, 1, idx[0], idx[1]));
        }
        throw new IllegalArgumentException("Invalid wire maps");
    }

    public String part2(WireMap m1, WireMap m2)
    {
        long steps = 0;
        for (Day03.WireMap.Coordinate c : m1.visitedCoords) {
            steps++;
            if (m2.checkXSect(c.x, c.y))
                return String.valueOf(steps + m2.getStepsTo(c.x, c.y));
        }
        throw new IllegalArgumentException("Invalid wire maps");
    }

    public static void main(String[] args)
    {
        Day03 day = new Day03();
        WireMap m1 = day.new WireMap(), m2 = day.new WireMap();
        try (Scanner sc = new Scanner(new File("input.txt"))){
            Stream.of(sc.next().split(",")).forEach(s -> m1.set(s));
            Stream.of(sc.next().split(",")).forEach(s -> m2.set(s));
            System.out.println(day.part1(m1, m2)); // 529
            System.out.println(day.part2(m1, m2)); // 20386
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
