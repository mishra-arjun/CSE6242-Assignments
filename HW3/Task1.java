package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Task1 {

    public static class GraphMapper extends Mapper<Object, Text, Text, IntWritable>{ 
    //Object is like the input file - like a json file. Format of the input data in the Object. 
    //Mapper is a class already defined. When we are calling these objects from the Mapper, we don't need to give names to them.
    //The input to the mapper is an object of type text and the output is a text and intwritable format.

//Map is also a method in the Mapper class.
    //The map always processes things one line at a time.
    public void map(Object key, Text value, Context context        
                    ) throws IOException, InterruptedException {

      String[] line_spl = value.toString().split("\t");
      //In Java, when we define a new object from a class, we define it with new TYPE(......
      context.write(new Text(line_spl[1]), new IntWritable(Integer.parseInt(line_spl[2])));
  //Output of the mapper is Text and Intwritable which is the input to the Reducer.

  public static class GraphReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      int fin = 0;
      for (IntWritable x : values) {
        if(fin < x.get()){
        	fin = x.get();
        }

      }
      result.set(fin);
      }
    }

      context.write(key, result);
    }
  }

public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Task1");

	job.setJarByClass(Task1.class);
	job.setMapperClass(GraphMapper.class);
	job.setReducerClass(GraphReducer.class);
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
