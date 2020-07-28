import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Stream;

public class Day02
{
    private static void runOp(Integer[] o, int opPos)
    {
        switch (o[opPos]) {
        case 1:
            o[o[opPos + 3]] = o[o[opPos + 1]] + o[o[opPos + 2]];
            break;
        case 2:
            o[o[opPos + 3]] = o[o[opPos + 1]]*o[o[opPos + 2]];
            break;
        default:
            throw new IllegalArgumentException(String.format("Unknown operation code: %d", o[opPos]));
        }
    }

    private static void init(Integer[] o, int noun, int verb)
    {
        o[1] = noun;
        o[2] = verb;
    }

    private static int runProgram(Integer[] operations, int noun, int verb)
    {
        init(operations, noun, verb);
        for (int i = 0; i < operations.length && operations[i] != 99; i += 4)
            runOp(operations, i);
        return operations[0];
    }

    public static String part1(List<Integer> values)
    {
        return String.valueOf(runProgram(values.toArray(new Integer[0]), 12, 2));
    }

    public static String part2(List<Integer> values)
    {
        for (int noun = 0; noun < 100; noun++)
            for (int verb = 0; verb < 100; verb++)
                if (runProgram(values.toArray(new Integer[0]), noun, verb) == 19690720)
                    return String.valueOf(100*noun + verb);
        throw new IllegalArgumentException("Final value not found");
    }

    public static void main(String[] args)
    {
        List<Integer> values = new ArrayList<>();
        try (Scanner sc = new Scanner(new File("input.txt"))) {
            while (sc.hasNext())
                Stream.of(sc.next().split(",")).map(n -> Integer.valueOf(n)).forEach(n -> values.add(n));
            System.out.println(part1(values)); // 6087827
            System.out.println(part2(values)); // 5379
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
